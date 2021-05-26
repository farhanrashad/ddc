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

    _name = 'partner.balance'

    start_date = fields.Date(
        string='From Date',
        required=True
    )
    end_date = fields.Date(
        string='To Date',
        required=True
    )
    partner_type = fields.Selection([
        ('receivable', 'Receivable Accounts'),
        ('payable', 'Payable Accounts'),
        ('all', 'Receivable & Payable Accounts'),
        ], string='Type',  default='all', required=True)
    
    is_posted = fields.Boolean('All Posted Entries', default=False)
    is_vendor_balance = fields.Boolean('Filter Partners with 0 Balance', default=False)
    category_id = fields.Many2one('res.partner.category', string='Select Category',)

    def print_report(self, data=None):
        data = {'start_date': self.start_date, 'end_date': self.end_date,'category_id': self.category_id.id,'partner_type': self.partner_type,'is_posted': self.is_posted, 'is_vendor_balance': self.is_vendor_balance}
        return self.env.ref('de_partner_balance.partner_balance_pdf').report_action(self, data=data)
