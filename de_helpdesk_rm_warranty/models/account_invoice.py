# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.move'
    
    warranty_count = fields.Integer(string='Warranty', compute='_compute_warranty_count')
    warranty_invoice_type = fields.Char(string='Invoice Type', compute='_compute_invoice_type', readonly=False)
    
    def _compute_invoice_type(self):
        wt = ''
        for invoice in self:
            for line in invoice.invoice_line_ids.sale_line_ids.repair_planning_line_id.warranty_id.warranty_type_id:
                wt = line.code
                line.warranty_invoice_type = wt
            if not invoice.warranty_invoice_type:
                invoice.warranty_invoice_type = 'R'
        
    def _compute_warranty_count(self):
        #warranty_ids = self.env['sale.warranty'].search([('barcode','=', self.barcode)])
        wc = 0
        for line in self.invoice_line_ids.sale_line_ids.repair_planning_line_id.warranty_id:
            wc += 1
        self.warranty_count = wc
        
    def action_view_warranty(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Warranty'),
            'res_model': 'sale.warranty',
            'view_mode': 'tree,form',
            'domain': [('barcode', '=', self.invoice_line_ids.sale_line_ids.repair_planning_line_id.warranty_id)],
        }
    

    