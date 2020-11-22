# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class InternalPaymentTransaction(models.Model):
    _name = 'internal.transaction'
    _rec_name = 'user_id'

    user_id = fields.Many2one(comodel_name='res.users', string='User')
    type = fields.Selection(
        [('transfer_in', 'Transfer In'),
         ('transfer_out', 'Transfer Out')],
        readonly=True, copy=False, string='Transaction Type')
