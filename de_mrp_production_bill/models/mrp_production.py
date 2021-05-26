# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date





class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    
    def get_bill_count(self):
        count = self.env['account.move'].search_count([('invoice_origin', '=', self.name)])
        self.bill_count = count
        
    bill_count = fields.Integer(string='Bill Count', compute='get_bill_count')
    
    
    def action_vendor_bill(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
#             'multi': False,
            'name': 'Vendor Bill',
            'domain': [('invoice_origin','in', self.name)],
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }
    

    def action_create_bill(self):
        for rec in self:
            selected_ids = rec.env.context.get('active_ids', [])
            selected_records = rec.env['mrp.production'].browse(selected_ids)
        return {
            'name': ('Production Bill'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'production.cost.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_production_ids': selected_records.ids},
        }
        
             
        
                
   
    partner_id = fields.Many2one('res.partner', string='Vendor',readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal', readonly=True)
    account_id = fields.Many2one('account.account', string='Expense Account', readonly=True)
    cost = fields.Float(string="Cost")
    

    
    
    

