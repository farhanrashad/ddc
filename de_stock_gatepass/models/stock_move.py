# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import ast
from datetime import timedelta, datetime

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning

from odoo.osv.expression import OR

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    gatepass_id = fields.Many2one('stock.gatepass',string='Gatepass', required=False)
    gatepass_qty = fields.Float(string='Gatepass Quantity',default=0)
    remaining_qty = fields.Float(string='Remaining Quantity',default=0, compute = 'compute_remain_qty')

    def compute_remain_qty(self):
        for rec in self:
            temp = rec.qty_done - rec.gatepass_qty
            rec.remaining_qty = temp