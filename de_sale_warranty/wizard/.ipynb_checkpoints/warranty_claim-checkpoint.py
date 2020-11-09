# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class WarrantyClaim(models.TransientModel):
    _name = 'sales.warranty.claim'
    _description = 'Warranty Claim'