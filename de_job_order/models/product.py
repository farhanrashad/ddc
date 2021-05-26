# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    sale_id = fields.Many2one("sale.order", string="Sale Order", store=True, readonly=False,)

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    sale_id = fields.Many2one("sale.order", string="Sale Order", store=True, readonly=False,)