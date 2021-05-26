from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp
import threading


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    stock_total_weight = fields.Float(string='Material Weight') 
    material_desc = fields.Char(related='bom_line_id.material_desc')
    
            
    
