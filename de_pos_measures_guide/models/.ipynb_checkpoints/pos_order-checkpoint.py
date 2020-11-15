# -*- coding: utf-8 -*-

from odoo import models, fields


class POSOrderLine(models.Model):
    """In this class a new model is created in pos to create measurement guide"""
    _inherit = 'pos.order.line'

    measure_note = fields.Char(string='Measurement Note',
                           help='Add measurment guide for POS order line')
