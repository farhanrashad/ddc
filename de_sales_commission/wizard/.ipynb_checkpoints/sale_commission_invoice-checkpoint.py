# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SalesCommissionInv(models.TransientModel):
    _name = "sale.commission.inv"
    _description = "Sales Commission Invoice"
    
    