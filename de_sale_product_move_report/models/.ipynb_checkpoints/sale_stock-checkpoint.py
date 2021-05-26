# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################

import time

from odoo import fields, api, models
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class SaleStockMove(models.TransientModel):
    _name = 'wizard.sale.stock.move'

    date = fields.Datetime(string='Stock Date', required=True, default=fields.Datetime.now )
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    location_id = fields.Many2one('stock.location', string='Select Location',required=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')
    group_by_report = fields.Selection([
        ('category', 'Product Category'),
        ('product', 'Product'),
        ('lot', 'Lot'),
        ], string='Group By',  default='product')
    filter_by_report = fields.Selection([
        ('sale', 'Sale'),
        ('location', 'Location'),
        ('vendor', 'Vendor'),
        ], string='Filter By',  default='sale')
    

    def print_report(self, data=None):
        data = {'date': self.date, 'location_id': self.location_id.id, 'location': self.location_id.name, 'sale_id': self.sale_id.id, 'sale': self.sale_id.name, 'partner_id': self.partner_id.id, 'group_by_report': self.group_by_report, 'filter_by_report': self.filter_by_report}
        return self.env.ref('de_sale_product_move_report.sale_stock_pdf').report_action(self, data=data)
