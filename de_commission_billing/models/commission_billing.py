# -*- coding: utf-8 -*-



from odoo import api, models,modules,fields, _
from odoo.exceptions import UserError

class resPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_a_broker = fields.Boolean(string="Is a Broker")
    commission_calculation_method = fields.Selection([
        ('by_rate_uom' , 'By Rate / UOM'),
        ('by_per_age','By %age of Total Amount')
    ], string='Commission Calculation Method')
    commission_rate = fields.Float(string = 'Commission Rate')
    commission_per = fields.Float(string = 'Commission %age')
    commission_paid_on_purchases_account = fields.Many2one('account.account', string='Commission Paid on Purchases Account')

    @api.onchange('is_a_broker')
    def check_name(self):
        if self.is_a_broker != True:
            self.commission_paid_on_purchases_account = False
            self.commission_calculation_method = False
            self.by_rate_uom = False
            self.commission_rate = 0
            self.by_per_age = False
            self.commission_per = 0

    @api.model
    def create(self, values):
        if values['is_a_broker']:
            if not values['commission_paid_on_purchases_account']:
                raise UserError(('Please select any commission paid account member!'))
            if not values['commission_calculation_method']:
                raise UserError(('Please choose (By Rate / UOM) OR (By %age of Total Amount) !'))
            else:
                if values['commission_calculation_method'] == 'by_rate_uom':
                    if values['commission_rate']<=0:
                        raise UserError(('Please Enter some Commission Rate value!'))
                if values['commission_calculation_method'] == 'by_per_age':
                    if values['commission_per']<=0:
                        raise UserError(('Please Enter some Commission %age value!'))
        return super(resPartnerInherit, self).create(values)

    def write(self, values):
        flag1 = 2
        flag2 = 2
        flag3 = 2
        flag4 = 2
        flag5 = 2
        try:
            val = values['is_a_broker']
            flag1 = 1
            if val == False:
                flag1 = 0
        except:
            pass

        try:
            val = values['commission_paid_on_purchases_account']
            flag2 = 1
            if not val:
                flag2 = 0
        except:
            pass

        try:
            val = values['commission_calculation_method']
            flag3 = 1
            if not val:
                flag3 = 0
        except:
            pass

        try:
            if flag3 == 1:
                if values['commission_calculation_method'] == 'by_rate_uom':
                    if values['commission_rate'] <= 0:
                        flag4 = 1
                    else:
                        values['commission_per'] = 0
                        flag4 = 0
            else:
                if values['commission_rate'] <= 0:
                    flag4 = 1
        except:
            pass

        try:
            if flag3 == 1:
                if values['commission_calculation_method'] == 'by_per_age':
                    if values['commission_per'] <= 0:
                        flag5 = 1
                    else:
                        values['commission_rate'] = 0
                        flag5 = 0
            else:
                if values['commission_per'] <= 0:
                    flag5 = 1
        except:
            pass

        if flag1 != 0:
            if flag2 == 0:
                raise UserError(('Please select any commission paid account member!'))
            elif flag3 == 0:
                raise UserError(('Please choose (By Rate / UOM) OR (By %age of Total Amount) !'))
            elif flag4 == 1:
                raise UserError(('Please Enter some Commission Rate value!'))
            elif flag5 == 1:
                raise UserError(('Please Enter some Commission %age value!'))
        return super(resPartnerInherit, self).write(values)
    

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    broker_partner_ref = fields.Many2one('res.partner',string="Broker" ,domain = [('is_a_broker','=',True)])
    commission_method = fields.Selection(related='broker_partner_ref.commission_calculation_method')

    def action_view_invoice(self):
        if self.broker_partner_ref.id:
            commission_rate_uom_bill = self.broker_partner_ref.commission_rate
            commission_percent_age_bill = self.broker_partner_ref.commission_per
            action = self.env.ref('account.action_move_in_invoice_type')
            result = action.read()[0]
            create_bill = self.env.context.get('create_bill', False)
            result['context'] = {
                'default_type': 'in_invoice',
                'default_company_id': self.company_id.id,
                'default_purchase_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_broker_partner_ref_bill' : self.broker_partner_ref.id,
                'default_commission_rate' : commission_rate_uom_bill,
                'default_commission_prcentage' : commission_percent_age_bill,
                'default_commission_method' : self.commission_method,
            }
        else:
            action = self.env.ref('account.action_move_in_invoice_type')
            result = action.read()[0]
            create_bill = self.env.context.get('create_bill', False)
            result['context'] = {
                'default_type': 'in_invoice',
                'default_company_id': self.company_id.id,
                'default_purchase_id': self.id,
                'default_partner_id': self.partner_id.id,
            }
        self.sudo()._read(['invoice_ids'])
        if len(self.invoice_ids) > 1 and not create_bill:
            result['domain'] = "[('id', 'in', " + str(self.invoice_ids.ids) + ")]"
        else:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                result['views'] = form_view
            if not create_bill:
                result['res_id'] = self.invoice_ids.id or False
        result['context']['default_invoice_origin'] = self.name
        result['context']['default_ref'] = self.partner_ref
        return result

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    
#     def unlink(self):
#         for move in self:
#             move.line_ids.unlink()
#         return super(AccountMoveInherit, self).unlink()
    


    broker_partner_ref_bill = fields.Many2one('res.partner',string="Broker" ,readonly=True, domain = [('is_a_broker','=',True)])
    commission_rate = fields.Float(string = 'Commission Rate')
    commission_prcentage = fields.Float(string = 'Commission %age')
    total_commission = fields.Float(compute='cal_total_commission',string = 'Total Commission')

    def cal_total_commission(self):
        if self.commission_prcentage:
            self.total_commission = float(self.amount_total) * (self.commission_prcentage/100)
        elif self.commission_rate:
            total_q = 0
            for record in self.invoice_line_ids:
                for rec in record:
                    total_q +=rec.quantity
            self.total_commission = float(total_q) * self.commission_rate
        else:
            self.total_commission = 0.00
            
            
    def button_cancel(self):              
        res = super(AccountMoveInherit, self).button_cancel()
        existing_entry = self.env['account.move'].search([('invoice_origin','=',self.name)])
        if existing_entry:
            existing_entry.button_cancel()
        return res        
            
    def button_draft(self):              
        res = super(AccountMoveInherit, self).button_draft()
        existing_entry = self.env['account.move'].search([('invoice_origin','=',self.name)])
        for entry in existing_entry:
            if entry:
                entry.button_draft()
                entry.line_ids.unlink()           
        return res

    def action_post(self):              
        res = super(AccountMoveInherit, self).action_post()
        existing_entry = self.env['account.move'].search([('invoice_origin','=',self.name)])
        if existing_entry:
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            move_dict = {
                          'journal_id': 2,
                          'type':'entry',
                          'ref': '',
                          'state': 'draft',
                          'date':self.date,
                          'partner_id' : self.broker_partner_ref_bill.id,
                          'invoice_origin': self.name,
                               }
                                    #step2:debit side entry
            debit_line = (0, 0, {
            
                                'name' : self.name ,
                                'debit' : abs(self.total_commission),
                                'credit' : 0.0,                   
                                'account_id' : self.broker_partner_ref_bill.commission_paid_on_purchases_account.id,
                                'partner_id' : self.broker_partner_ref_bill.id,

                        })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                            #step3:credit side entry
            credit_line = (0, 0, {
                              'name': self.name,
                              'debit': 0.0,
                              'credit': abs(self.total_commission),
                              'account_id': self.broker_partner_ref_bill.property_account_payable_id.id,
                              'partner_id' : self.broker_partner_ref_bill.id,

                })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = existing_entry.write(move_dict)

            existing_entry.action_post()
        else:
            if self.type == 'in_invoice' and self.broker_partner_ref_bill:
                line_ids = []
                debit_sum = 0.0
                credit_sum = 0.0
                move_dict = {
                          'journal_id': 2,
                          'type':'entry',
                          'ref': '',
                          'state': 'draft',
                          'date':self.date,
                          'partner_id' : self.broker_partner_ref_bill.id,
                          'invoice_origin': self.name,
                               }
                                    #step2:debit side entry
                debit_line = (0, 0, {
            #                 	'move_id': self.id,
                                'name' : self.name ,
                                'debit' : abs(self.total_commission),
                                'credit' : 0.0,                   
                                'account_id' : self.broker_partner_ref_bill.commission_paid_on_purchases_account.id,
                                'partner_id' : self.broker_partner_ref_bill.id,

                        })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                            #step3:credit side entry
                credit_line = (0, 0, {
            #                   'move_id': self.id,
                              'name': self.name,
                              'debit': 0.0,
                              'credit': abs(self.total_commission),
                              'account_id': self.broker_partner_ref_bill.property_account_payable_id.id,
                              'partner_id' : self.broker_partner_ref_bill.id,

                })
                line_ids.append(credit_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

                move_dict['line_ids'] = line_ids
                move = self.env['account.move'].create(move_dict)

                move.post()
                
                self.message_post(body=_('Journal Entry Number : %s, ') % (move.name,),
                          partner_ids=[self.env.user.partner_id.id])
                
            
            
        return res

 