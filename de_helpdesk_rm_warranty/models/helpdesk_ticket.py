# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    warranty_count = fields.Integer(string='Warranty', compute='_compute_warranty_count')
    
    def _compute_warranty_count(self):
        wc = 0
        for line in self.workorder_ids.order_ids.warranty_ids:
            wc += 1
        self.warranty_count = wc
        
    def action_view_warranty(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Warranty'),
            'res_model': 'sale.warranty',
            'view_mode': 'tree,form',
            'domain': [('sale_id', 'in', self.workorder_ids.order_ids.ids)],
            #'context': dict(self._context, create=False, default_sale_id=self.id),
        }