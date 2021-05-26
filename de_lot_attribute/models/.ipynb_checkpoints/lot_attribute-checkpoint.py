# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    lot_attribute_ids = fields.One2many('stock.production.lot.attribute', 'lot_id', string='Lot Attribute Ids', copy=True, auto_join=True)
    
    #@api.depends('lot_attribute_ids')
    #def _amount_all(self):


class StockProductionLotAttribute(models.Model):
	_name = 'stock.production.lot.attribute'
	_description = 'Stock Production Lot Attribute'
	
	lot_id = fields.Many2one('stock.production.lot', string='Lot', index=True, required=True, ondelete='cascade')
	attribute_id = fields.Many2one('product.attribute', string='Attribute', required=True, index=True)
	attribute_value_id = fields.Many2one('product.attribute.value', string='Attribute Value', required=True, index=True)
