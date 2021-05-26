# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class PickingGatepass(models.Model):
    _inherit = 'stock.picking'
    
    driver_name = fields.Char('Driver')
    vehicle_no = fields.Char('Vehicle No.')
    gatepass_no = fields.Char('Gatepass No.')
    