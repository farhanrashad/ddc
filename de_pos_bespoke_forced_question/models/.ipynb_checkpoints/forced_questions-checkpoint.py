# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


class POSForcedQuestion(models.Model):
    _inherit = 'pos.forced.question'

    product_property_line_id =fields.Many2one("product.properties.line",string="Property Line")
    product_property_description =fields.Char(related="product_property_line_id.description",string="Description")
    product_property_is_short =fields.Boolean(string='Is Short', readonly=True, compute="_get_property_value")
    product_property_is_long =fields.Boolean(string='Is Long', readonly=True, compute="_get_property_value")

    product_id =fields.Many2one("product.product",string="Product")
    product_uom_id = fields.Many2one('uom.uom',related='product_id.uom_id', string='UOM')
    product_qty = fields.Float(string='Quantity')

    @api.depends('product_property_line_id.product_property')
    def _get_property_value(self):
        for line in self:
            line.product_property_is_short = line.product_property_line_id.product_property.is_short
            line.product_property_is_long = line.product_property_line_id.product_property.is_long