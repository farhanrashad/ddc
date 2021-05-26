# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplateRef(models.Model):
    _inherit = 'product.template'
    
    ref_product_tmpl_id = fields.Many2one('product.template', 'Product Reference', stored=True, required=False)

class ProductProductRef(models.Model):
    _inherit = 'product.product'
    
    ref_product_id = fields.Many2one('product.product', 'Variant Reference', stored=True, required=False)