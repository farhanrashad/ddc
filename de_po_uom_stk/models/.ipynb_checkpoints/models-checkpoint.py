# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    po_uom_stk = fields.Float(string='S Stock', readonly=False, compute='_calculate_po_uom_stock', default=0.0)
    
    def _calculate_po_uom_stock(self):
        for rs in self:
            if rs.uom_po_id.uom_type == 'bigger':
                rs.po_uom_stk = rs.qty_available / rs.uom_po_id.factor_inv
            elif rs.uom_po_id.uom_type == 'smaller':
                rs.po_uom_stk = rs.qty_available * rs.uom_po_id.factor_inv
            else:
                rs.po_uom_stk = rs.qty_available