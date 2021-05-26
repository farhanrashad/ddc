# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from num2words import num2words


class JeChequePrint(models.Model):
    _inherit = 'account.move'

    is_cheque_print = fields.Boolean(string='Cheque Print', default=False)
    payee = fields.Char(string='Payee')
    amount = fields.Float(string='Amount')
    cheque_formate_id = fields.Many2one('cheque.setting', string='Cheque Format')
    amount_in_words = fields.Char(string='Amount in Words')
    
    
    @api.model
    def get_date(self,date):
        date = str(date).split('-')
        return date
    
    @api.onchange('amount')
    def _amount_word(self):
        amt_word = num2words(self.amount)
        self.amount_in_words = amt_word