# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_charge = fields.Boolean(string='Is Charge', store=True)

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
            'domain': [('invoice_origin','=', self.name)],
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }
    
    
    def button_generate_bill(self):
        product_list = []
        for line in self:
            product_list.append((0,0, {
                    'name': line.name,
                    'account_id': line.account_id.id,
                    'quantity': line.product_qty, 
                    'price_unit': line.cost,
                    'partner_id': self.partner_id.id,
                        }))
                        
        vals = {
                'partner_id': self.partner_id.id,
                'journal_id': self.journal_id.id,
                'invoice_date': fields.Date.today(),
                'type': 'in_invoice',
                'invoice_origin': self.name,
                'invoice_line_ids': product_list   
                }
        move = self.env['account.move'].create(vals)     
        
                
    def _get_default_journal(self):
        return self.env['account.journal'].search([
            ('type', '=', 'purchase'),],
            limit=1).id   
    
    def _get_default_account(self):
        return self.env['account.account'].search([
            ('id', '=', 111),],
            limit=1).id 
    
    partner_id = fields.Many2one('res.partner', string='Vendor')    
    journal_id = fields.Many2one('account.journal', string='Journal', default=_get_default_journal)
    account_id = fields.Many2one('account.account', string='Expense Account', default=_get_default_account)
    cost = fields.Float(string="Cost")
    production_id = fields.Many2one('mrp.production', string="Manufacturing Order")
    

    
    
    

