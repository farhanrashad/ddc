# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductionTolerance(models.Model):
    _name = 'mrp.job.order.tolerance'
    _description = 'ProductionTolerance'

    name = fields.Char(string='Name', required=True)
    percentage_qty = fields.Float(string='Quantity In Percentage')
