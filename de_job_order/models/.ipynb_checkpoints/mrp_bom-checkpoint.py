# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    categ_id = fields.Many2one("product.category", related='product_tmpl_id.categ_id', string="Category", readonly=True)
    
    compute_qty = fields.Selection([
        ('qty', 'By Quantity'),
        ('percentage', 'By Percentage'),
        ], index=True, default='qty', required=True)
    
    def _recursive_boms(self):
        """
        @return: returns a list of tuple (id) which are all the children of the passed bom_ids
        """
        children_boms = []
        for bom in self.filtered(lambda bom: bom.bom_line_ids.product_id.product_tmpl_id.bom_ids):
            children_boms += bom.bom_line_ids.product_id.product_tmpl_id.bom_ids._recursive_boms()
        return [(bom.id) for bom in self] + children_boms


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    percent_qty = fields.Float('Percentage Quantity')
    material_desc = fields.Char('Componenet Description')

    @api.onchange('percent_qty')
    def _onchange_percent_qty(self):
        for rs in self:
            if rs.bom_id.compute_qty == 'percentage':
                if rs.percent_qty > 0:
                    rs.product_qty = rs.bom_id.product_qty * (rs.percent_qty / 100)