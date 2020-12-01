# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

class AccountMove(models.Model):
    _inherit = 'account.move'

    bespoke_order_id = fields.Many2one('pos.bespoke.order', string='Bespoke Order', index=True, ondelete='cascade')



