# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    sec_uom_id = fields.Many2one('uom.uom', string='Secondary UOM')
    sec_uom_factor = fields.Float('Factor',default='1.0')
    sec_qty = fields.Float('Sec. Qty', compute='_calculate_secondary_qty', readonly=True)
    
    @api.depends('qty_available')
    def _calculate_secondary_qty(self):
        for rs in self:
            #rs.sec_qty = 1
            #if rs.sec_uom_id.id and rs.sec_uom_factor:
            rs.sec_qty = rs.qty_available * rs.sec_uom_factor