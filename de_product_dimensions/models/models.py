# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class Product(models.Model):
    _inherit = 'product.template'

    weight_sm = fields.Integer(string='GSM')
    width = fields.Integer(string='Width')
    length = fields.Integer(string='Length')
    height = fields.Integer(string='Height')
    dim_weight = fields.Float(string='Weight/Kg',digits=dp.get_precision('Stock Weight'))