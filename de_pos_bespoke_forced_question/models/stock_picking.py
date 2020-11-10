# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    bespoke_order_id = fields.Many2one('pos.bespoke.order', string='Bespoke Order', index=True, ondelete='cascade')



