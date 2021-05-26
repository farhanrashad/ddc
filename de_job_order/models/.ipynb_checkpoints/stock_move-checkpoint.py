# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    ref_job_order_id = fields.Many2one("job.order", compute="_assign_sale_order", store=False, string="Job Order", readonly=True, required=False,oldname="job_order_id")
    ref_sale_id = fields.Many2one("sale.order",compute="_assign_sale_order", store=False, readonly=True,)
    job_order_id = fields.Many2one("job.order", related="ref_job_order_id", string="Job Order", readonly=True, store=True)
    sale_id = fields.Many2one("sale.order", related="ref_sale_id", string="Sale Order", readonly=True, store=True)
    
    subcontract_order_line_id = fields.Many2one('purchase.order.line', 'Subcontract Order Line', domain="['|', ('order_id.job_order_id', '=', ref_job_order_id), ('order_id.job_order_id', '=', job_order_id) ]")
    
    @api.model
    def _assign_sale_order(self):
        #picking_id = self.id
        for line in self:
            query = """
        select max(a.job_order_id) as job_order_id, max(a.sale_id) as sale_id from (
        select p.job_order_id,j.sale_id from purchase_order p
left join job_order j on j.id = p.job_order_id
where p.id = %(purchase_id)s 
union all
select j.id as job_order_id, s.id as sale_id from sale_order s
left join job_order j on j.sale_id = s.id
where s.id = %(sale_id)s
union all
select m.job_order_id, j.sale_id from mrp_production m
join job_order j on m.job_order_id = j.id
where m.id = %(production_id)s
) a
            """
            """
            union all
select m.job_order_id, m.ref_sale_id as sale_id from stock_move m 
left join stock_picking k on m.picking_id = k.id
where m.reference = %(picking_ref)s or k.name = %(picking_ref)s
            """
            picking = self.env['stock.picking'].search([('name', '=', line.group_id.name)],limit=1)
            stock_move = self.env['stock.move'].search([('reference', '=', line.group_id.name)],limit=1)
            
            params = {
                'purchase_id': line.purchase_line_id.order_id.id or 0,
                'sale_id': line.sale_line_id.order_id.id or 0,
                'picking_ref': line.group_id.name or '',
                'production_id':line.production_id.id or 0,
            }
            self.env.cr.execute(query, params=params)
            #cr = self._cr
            for order in self._cr.dictfetchall():
                line.update ({
                    'ref_job_order_id': order['job_order_id'] or picking.job_order_id.id or stock_move.job_order_id.id,
                    'ref_sale_id': order['sale_id'] or picking.ref_sale_id.id or stock_move.ref_sale_id.id,
                })
                
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
       
    @api.depends('qty_done')
    def _calculate_all_dummy_qty(self):
        for line in self:
            if line.location_id.usage == 'internal':
                line.out_qty_d = line.qty_done
            elif line.location_dest_id.usage == 'internal':
                line.in_qty_d = line.qty_done
                
    ref_job_order_id = fields.Many2one("job.order", compute="_compute_move_reference_order", store=True, string="Reference Job Order", readonly=True)
    ref_sale_id = fields.Many2one("sale.order", related="move_id.ref_sale_id", string="Reference Sale", store=True, readonly=True,)
    
    job_order_id = fields.Many2one("job.order", string="Job Order", readonly=True, store=True)
    sale_id = fields.Many2one("sale.order", string="Sale Order", readonly=True, store=True)
    
    
    
    @api.depends('move_id')
    def _compute_move_reference_order(self):
        for line in self:
            line.ref_job_order_id = line.move_id.ref_job_order_id or line.move_id.job_order_id
    
    