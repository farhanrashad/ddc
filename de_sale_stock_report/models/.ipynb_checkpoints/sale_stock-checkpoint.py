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


class PartnerLedger(models.TransientModel):
    _name = 'sale.stock'

    date = fields.Datetime(string='Stock Date', required=True, default=fields.Datetime.now )
    sale_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    location_id = fields.Many2one('stock.location', string='Select Location',required=True)
    group_by_report = fields.Selection([
        ('product', 'Product'),
        ('lot', 'Lot'),
        ], string='Group By',  default='product')
    

    def print_report(self, data=None):
        data = {'date': self.date, 'location_id': self.location_id.id, 'location': self.location_id.name, 'sale_id': self.sale_id.id, 'sale': self.sale_id.name, 'group_by_report': self.group_by_report}
        return self.env.ref('de_sale_stock_report.sale_stock_pdf').report_action(self, data=data)
