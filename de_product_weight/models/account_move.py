# -*- coding: utf-8 -*-
from odoo import models,fields,api,_

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    is_sale_weight = fields.Boolean(related='partner_id.is_sale_weight',string='Enable Weight Pricing',readonly=True)
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=True, store=True)
    total_weight = fields.Float(string='Total Weight',default=1.0, readonly=False, store=True)
    price_weight = fields.Float(string='Price Weight', readonly=False, store=True, digits='Product Price')
    
    #price_qty_weight = fields.Float(string='Price Qty/Weight', store=False, digits='Product Price',compute='_compute_price_weight')
    
    @api.depends('quantity', 'weight')
    def _compute_total_weight(self):
        for line in self:
            line.total_weight = line.quantity * line.weight
    
    @api.depends('product_id', 'weight')
    def _compute_price_weight(self):
        price = 0
        for line in self:
            for price in line.sale_line_ids:
                price = price.price_weight
            line.update({
                'price_weight': price
            })
            
    @api.onchange('price_weight')
    def _onchange_price_unit(self):
        #res = super(AccountMoveLine, self).product_id_change()
        for line in self:
            if line.quantity > 0:
                line.price_unit = (line.total_weight * line.price_weight) / line.quantity
        #return res
                    
            #if line.quantity > 0:
                #line.price_qty_weight = (line.total_weight * line.price_weight) / line.quantity
                
    @api.onchange('quantity','weight')
    def _onchange_weight(self):
        for line in self:
            line.total_weight = line.weight * line.quantity
            
    
            
