from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_agent = fields.Boolean(string='Is a Agent')
    agent_id = fields.Many2one('res.partner', string='Agent', domain="[('is_agent','=',True),('id','!=',id)]")
    

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one(related='partner_id.agent_id')
    

class AccountInvoiceInherit(models.Model):
    _inherit = 'account.move'
    

    
    @api.model
    def action_create_bill(self):
        agent_list = []
        for invoice in self:
            if invoice.agent_id and invoice.commission_settled == False:
                agent_list.append(invoice.agent_id)
                
        list = set(agent_list)
        product_list = []
        for agent in list:
            total_commission_amount = 0
            for agent_invoice in self:
                if  agent_invoice.agent_id.id ==  agent.id  and agent_invoice.commission_settled == False:
                    total_commission_amount = total_commission_amount + agent_invoice.commission  
                    
                agent_invoice.update({
                'commission_settled': True,
                })


            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            move_dict = {
    #               'name' : self.name, 
                  'journal_id': 2,
                  'type': 'in_invoice', 
                  'date': fields.Date.today(),
                  'state': 'draft',
                       }
                            #step2:debit side entry
            debit_line = (0, 0, {
                               'name':  'Commission Bill',
                                'debit': 100,
                                'credit': 0.0,
                                'partner_id': 4438,
                                'account_id': 13,
                             })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                    #step3:credit side entry
            credit_line = (0, 0, {
                                'name': 'Commission Bill',
                                'debit': 0.0,
                                'credit': 100,
                                'partner_id': 4438,
                                'account_id': 14,
                              })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)   



        
        

    agent_id = fields.Many2one(related='partner_id.agent_id')
    commission_rate = fields.Float(string='Commission Rate')
    commission = fields.Float(string='Commission', compute='compute_commission')
    commission_settled = fields.Boolean(string="Commission Settled", readonly=True)
    
    @api.onchange('invoice_line_ids.quantity')
    def compute_commission(self):
        for record in self:
            total_quantity = 0
            total_commission_rate = 0
            for line in record.invoice_line_ids:
#                 if line.package_id.shipping_grade == 'fresh':
                total_quantity = total_quantity + line.quantity
                total_commission_rate = total_commission_rate + line.commission_rate  
            record.commission = total_quantity * total_commission_rate
            
            
class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    commission_rate = fields.Float(string='Commission Rate')            
