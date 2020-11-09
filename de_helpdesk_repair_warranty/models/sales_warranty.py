# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SalesWarranty(models.Model):
    _inherit = 'sales.warranty'
    
    repair_id = fields.Many2one('repair.order', string='Repair Order', readonly=True)
