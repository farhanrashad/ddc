# -*- coding: utf-8 -*-

from odoo import models, fields


class POSConfig(models.Model):
    _inherit = 'pos.config'

    iface_orderline_order_measures_notes = fields.Boolean(string='Orderline Measurement', help='Allow measurement on Orderlines.')
