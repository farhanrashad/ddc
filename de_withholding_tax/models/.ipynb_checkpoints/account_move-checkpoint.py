# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    is_wht_line = fields.Boolean(string='Withholding Tax Line',readonly=True, default=False)
    is_wht_paid = fields.Boolean(string='Withholding Tax Paid',readonly=True, default=False)