# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=False, store=True,default=1.0)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), store=True, readonly=True, compute="_calculate_total_weight", help="Weight of the product in order line",default=1.0)
    price_weight = fields.Float('Weight Price', required=True, digits=dp.get_precision('Weight Price'), default=1.0)
    #price_weight_subtotal = fields.Float(compute='_compute_weight_subtotal', string='Subtotal', readonly=True, store=True)
    
    @api.depends('product_uom_qty', 'weight')
    def _calculate_total_weight(self):
        for line in self:
            line.total_weight = line.product_uom_qty * line.weight

    @api.onchange('product_id','product_uom_qty','weight')
    def _onchange_quantity(self):
        for rec in self:
            rec.total_weight = rec.weight * rec.product_uom_qty
    
    @api.onchange('price_weight')
    def _onchange_price_unit(self):
        res = super(SaleOrderLine, self).product_id_change()
        for line in self:
            if line.product_uom_qty > 0:
                line.price_unit = (line.total_weight * line.price_weight) / line.product_uom_qty
        return res

        
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    sum_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=False, readonly=True)
    sum_weight = fields.Float(string='Total Weight', compute='_quantity_all', store=False, readonly=True)
    is_sale_weight = fields.Boolean(related='partner_id.is_sale_weight',string='Compute prices in weight',readonly=True)
    
    @api.depends('order_line.product_uom_qty','order_line.total_weight')
    def _quantity_all(self):
        """
        Compute the total Quantity and Weight of the SO.
        """
        sum_qty = sum_weight = 0.0
        for order in self:
            sum_qty = sum_weight = 0.0
            for line in order.order_line:
                sum_qty += line.product_uom_qty
                sum_weight += (line.weight * line.product_uom_qty)
            order.sum_qty = sum_qty
            order.sum_weight = sum_weight
            
            
