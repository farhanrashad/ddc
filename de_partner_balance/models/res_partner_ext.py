# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountPartnerBalance(models.Model):
    _inherit = 'res.partner'

    def _get_accounting_balance(self):
        move_lines = self.env['account.move.line'].search([('partner_id', '=', self.id)])
        bal = 0
        for line in move_lines:
            if line.move_id.state == 'posted':
                bal = bal + (line.debit - line.credit)
        partner = self.env['res.partner'].search([('id', '=', self.id)])
        partner.update({'account_balance': bal})

    account_balance = fields.Float(string='Account Balance', compute='_get_accounting_balance')
