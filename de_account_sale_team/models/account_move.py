# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('invoice_line_ids.categ_id')
    def onchange_partner_id(self):
        super(AccountMove, self).onchange_categ_id()
        self.agent_id = self.partner_id.agent_id or False
        self.commission_percentage = self.partner_id.commission_percent


# class de_account_sale_team(models.Model):
#     _name = 'de_account_sale_team.de_account_sale_team'
#     _description = 'de_account_sale_team.de_account_sale_team'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
