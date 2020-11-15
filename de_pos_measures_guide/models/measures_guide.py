# -*- coding: utf-8 -*-

from odoo import models, fields


class POSMeasuresGuide(models.Model):
    """In this class a new model is created in pos to create measurement guide"""
    _name = 'pos.order.measures'

    name = fields.Char(string='Measurement Item',
                           help='Add measurment guide for POS order line')
