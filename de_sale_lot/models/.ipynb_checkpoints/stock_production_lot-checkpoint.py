# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    sale_id = fields.Many2one("sale.order", readonly=False)
    partner_id = fields.Many2one("res.partner", related="sale_id.partner_id", string="Partner", readonly=True, store=True)
