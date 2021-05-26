# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class MRPProduction(models.Model):
    _inherit = 'mrp.production'
    
    product_sec_qty = fields.Float(string='Total Sec. Qty',compute='_calculate_total_sec_qty')
    
    def _calculate_total_sec_qty(self):
        for rs in self:
            if rs.product_id.sec_uom_id:
                rs.product_sec_qty = rs.product_uom_qty * rs.product_id.sec_uom_factor
    
    