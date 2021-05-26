# -*- coding: utf-8 -*-

import time

import datetime

from datetime import datetime, date, time 

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    entry_date = fields.Date('Created Date', compute='_compute_manual_dates', readonly=True)
    delivery_date = fields.Date('Delivery Date', compute='_compute_manual_dates',readonly=True)
    
    def _compute_manual_dates(self):
        for line in self:
            line.update({
               'entry_date': line.create_date,
                'delivery_date': line.commitment_date,
            }) 
