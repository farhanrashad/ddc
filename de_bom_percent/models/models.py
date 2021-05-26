# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    compute_qty = fields.Selection([
        ('qty', 'By Quantity'),
        ('percentage', 'By Percentage'),
        ], index=True, default='qty', required=True)
    

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    percent_qty = fields.Float('Percentage Quantity')

    @api.onchange('percent_qty')
    def _onchange_percent_qty(self):
        for rs in self:
            if rs.bom_id.compute_qty == 'percentage':
                if rs.percent_qty > 0:
                    rs.product_qty = rs.bom_id.product_qty * (rs.percent_qty / 100)