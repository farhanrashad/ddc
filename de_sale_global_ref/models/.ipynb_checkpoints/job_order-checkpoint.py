# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class JobOrder(models.Model):
    _inherit = 'job.order'
    
    global_ref = fields.Char(related='sale_id.global_ref', string='Global Reference', store=True)