from odoo import api, fields, models, _
from odoo.exceptions import UserError

    
class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    bank_statement_entry = fields.Boolean(string='Add Bank Statement Entry')
    bank_statement = fields.Many2one('account.bank.statement')
    
    def post(self):
        payments_need_trans = self.filtered(lambda pay: pay.payment_token_id and not pay.payment_transaction_id)
        transactions = payments_need_trans._create_payment_transaction()
        res = super(AccountPaymentInherit, self - payments_need_trans).post()
        data = []
        flag = 0
        payment_amount = 0
        payment_name = ''
        
        if self.partner_type == 'supplier':
            payment_amount = self.amount * (-1)
        else:
            payment_amount = self.amount
        
        if self.communication:
            payment_name = self.communication
        else:
            payment_name = self.name
        
        for i in self.bank_statement.line_ids:
            if self.name == i.name:
                flag = 1
                i.payment_date = self.payment_date
                i.name = payment_name
                i.partner_id = self.partner_id.id
                i.ref = self.name
                i.amount = payment_amount
        if not flag:        
            data.append((0, 0, {
                    'date': self.payment_date,
                    'name': payment_name,
                    'partner_id': self.partner_id.id,
                    'ref': self.name,
                    'amount': payment_amount,
                }))
            
        self.bank_statement.line_ids = data
        transactions.s2s_do_transaction()
        return res
        
