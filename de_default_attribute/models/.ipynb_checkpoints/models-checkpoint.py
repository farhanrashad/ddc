# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    attribute_id = fields.Many2one('product.attribute', string='Attribute', required=False, index=True)