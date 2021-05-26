# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Dynexcel Business Solution <www.dynexcel.com>

#
#################################################################################

from odoo import api, fields, models, _

class SaleCommissionWizard(models.TransientModel):
    _name = "sale.commission.wizard"
    _description = "Sale Commission wizard"
    
    invoice_ids = fields.Many2many('account.move', string="Production")
    
    
    def create_bill(self):    
        agent_list = []
        for invoice in self.invoice_ids:
            if invoice.agent_id and invoice.commission_settled == False:
                agent_list.append(invoice.agent_id)
                
        list = set(agent_list)
        product_list = []
        for agent in list:
            total_commission_amount = 0
            for agent_invoice in self.invoice_ids:
                if  agent_invoice.agent_id.id ==  agent.id  and agent_invoice.commission_settled == False:
                    total_commission_amount = total_commission_amount + agent_invoice.commission  
                    
#                 invoice.update({
#                 'commission_settled': True,
#                 })  
        commission_list = []
        commission_list.append((0,0, {
                        'name': 'Commission Bill',
                        'account_id': 13,
                        'quantity': 1, 
                        'price_unit': 20,
                        'partner_id': 4438,
                            }))

        vals = {
                'partner_id': 4438,
                'journal_id': 2,
                'invoice_date': fields.Date.today(),
                'type': 'in_invoice',
                'invoice_origin': 'Commission',
                'amount_total': 100, 
                'invoice_line_ids': commission_list,   
                    }
        move = self.env['account.move'].create(vals)
        
    
    
