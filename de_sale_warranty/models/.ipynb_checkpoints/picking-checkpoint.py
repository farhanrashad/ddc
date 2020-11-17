# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    warranty_ids = fields.One2many('sale.warranty', 'sale_id', string='Warranty')
    warranty_count = fields.Integer(string='Warranty', compute='_compute_warranty_count')
    
    @api.depends('warranty_ids')
    def _compute_warranty_count(self):
        warranty_data = self.env['sale.warranty'].sudo().read_group([('picking_id', 'in', self.ids)], ['picking_id'], ['picking_id'])
        mapped_data = dict([(r['picking_id'][0], r['picking_id_count']) for r in warranty_data])
        for line in self:
            line.warranty_count = mapped_data.get(line.id, 0)
    
    def action_view_warranty(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Warranty'),
            'res_model': 'sale.warranty',
            'view_mode': 'tree,form',
            'domain': [('picking_id', '=', self.id)],
            'context': dict(self._context, create=False, default_picking_id=self.id),
        }
            
    def action_done(self):
        res = super(StockPicking, self).action_done()
        vals = {}
        start_date = end_date = datetime.date.today()
        for line in self.move_line_ids_without_package:
            if line.product_id.product_tmpl_id.is_warranty and line.product_id.product_tmpl_id.warranty_policy == 'delivery':
                if line.product_id.product_tmpl_id.warranty_period == 'y':
                    end_date = start_date + datetime.timedelta(days=(line.product_id.product_tmpl_id.warranty_period_interval*365))
                elif line.product_id.product_tmpl_id.warranty_period == 'm':
                    end_date = start_date + datetime.timedelta(days=(line.product_id.product_tmpl_id.warranty_period_interval*30))
                elif line.product_id.product_tmpl_id.warranty_period == 'd':
                    end_date = start_date + datetime.timedelta(days=(line.product_id.product_tmpl_id.warranty_period_interval))
                vals = {
                    'product_id': line.product_id.id,
                    'partner_id': self.partner_id.id,
                    'sale_id': self.sale_id.id,
                    'picking_id': self.id,
                    'warranty_start_date':start_date,
                    'warranty_end_date': end_date,
                    'state':'draft',
                }
                warranty_id = self.env['sale.warranty'].create(vals)
        return res
    
    def action_cancel(self):
        res = super(StockPicking, self).action_cancel()
        for line in self.warranty_ids:
            line.update({
                'state': 'cancel'
            })
        return res