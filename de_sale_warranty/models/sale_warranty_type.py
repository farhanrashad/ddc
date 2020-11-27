# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SaleWarrantyType(models.Model):
    _name = 'sale.warranty.type'
    _description = 'Sale Warranty Type'
    
    name = fields.Char(string='Name', required=True)
    warranty_period = fields.Integer(string='Warranty Period', required=True)
    warranty_unit = fields.Selection([('year','Year(s)'),('month','Month(s)'),
                                      ('day','Day(s)'),],string = "Unit", default='year',track_visibility='onchange', required=True)

    warranty_note = fields.Text(string='Note')