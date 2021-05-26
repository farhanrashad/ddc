# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Dynexcel Business Solution <www.dynexcel.com>

#
#################################################################################

from odoo import api, fields, models, _

class ProductionCostWizard(models.TransientModel):
    _name = "production.cost.wizard"
    _description = "Production Cost wizard"
    
    def _get_default_journal(self):
        return self.env['account.journal'].search([
            ('type', '=', 'purchase'),],
            limit=1).id   
    
    def _get_default_partner(self):
        return self.env['res.partner'].search([
            ('id', '=', 1873),],
            limit=1).id  
    
    def _get_default_account(self):
        return self.env['account.account'].search([
            ('id', '=', 111),],
            limit=1).id 
            
    
    
    
    partner_id = fields.Many2one('res.partner', string='Vendor', default=_get_default_partner)    
    journal_id = fields.Many2one('account.journal', string='Journal', default=_get_default_journal)
    account_id = fields.Many2one('account.account', string='Expense Account', default=_get_default_account)
    cost = fields.Float(string="Cost")
    production_ids = fields.Many2many('mrp.production', string="Production")
    
    
    def action_create_bill(self):
        production_order = ' '
        sum_production_quantity = 0.0
        for production in self.production_ids:
            production_order += production.name + ' '
            sum_production_quantity = sum_production_quantity + production.product_qty
            production.update({
                'partner_id': self.partner_id.id,
                'journal_id': self.journal_id.id,
                'account_id': self.account_id.id,
                'cost': self.cost,
            })
                           
        product_list = []
        product_list.append((0,0, {
                    'name': 'Production Bill',
                    'account_id': self.account_id.id,
                    'quantity': sum_production_quantity, 
                    'price_unit': self.cost,
                    'partner_id': self.partner_id.id,
                        }))
                        
        vals = {
                'partner_id': self.partner_id.id,
                'journal_id': self.journal_id.id,
                'invoice_date': fields.Date.today(),
                'type': 'in_invoice',
                'invoice_origin': production_order,
                'invoice_line_ids': product_list   
                }
        move = self.env['account.move'].create(vals)
        
    
    
