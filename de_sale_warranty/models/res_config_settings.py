# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    default_warranty_policy = fields.Selection([
        ('order', 'Warranty start on order confirmation'),
        ('delivery', 'Warranty start on delivery')
        ], 'Warranty Policy',
        default='order',
        default_model='product.template')
    
    default_warranty_period = fields.Selection([
        ('d', 'Day(s)'),
        ('m', 'Month(s)'),
        ('y', 'Year(s)'),
        ], 'Warranty period',
        default='d',
        default_model='product.template')
    
    warranty_period_interval = fields.Integer(related='company_id.warranty_period_interval', required=True, readonly=False)