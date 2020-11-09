# -*- coding: utf-8 -*-

import json
import logging

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    warranty_period_interval = fields.Integer(string='Period Interval',store=True, copy=True)