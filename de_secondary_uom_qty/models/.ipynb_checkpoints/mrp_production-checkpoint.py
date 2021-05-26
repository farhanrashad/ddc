# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class MRPsecProduction(models.Model):
    _inherit = 'mrp.production'
    
    product_sec_qty = fields.Float(string='Total Sec. Qty',compute='_calculate_total_sec_qty',default=0)
    
    def _calculate_total_sec_qty(self):
        for rs in self:
            #rs.product_sec_qty = 10
            if rs.product_id.product_tmpl_id.sec_uom_id and rs.product_id.product_tmpl_id.sec_uom_factor > 0:
                rs.product_sec_qty = rs.product_qty * rs.product_id.product_tmpl_id.sec_uom_factor
            else:
                rs.product_sec_qty = 0
    
    