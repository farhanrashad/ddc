# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    sale_id = fields.Many2one("sale.order", related="lot_id.sale_id", string="Sale Order")
