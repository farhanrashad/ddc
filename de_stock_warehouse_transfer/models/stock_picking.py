# -*- coding: utf-8 -*-
from datetime import date
import time
from odoo import models, fields, api, _
from odoo import exceptions 
from odoo.exceptions import UserError, ValidationError




class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    warehouse_transfer_id = fields.Many2one('stock.warehouse.transfer', 'Warehouse Transfer', )
