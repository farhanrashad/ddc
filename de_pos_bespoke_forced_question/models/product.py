# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_bespoke = fields.Boolean(string='Allowed Bespoke',
                                 help="Check if the product should be bespoke order")


