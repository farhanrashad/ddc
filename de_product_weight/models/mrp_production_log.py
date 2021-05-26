# -*- coding: utf-8 -*-
from odoo import models,fields,api,_

from odoo.addons import decimal_precision as dp


class MrpProductionLog(models.Model):
    _name = 'mrp.production.log'

    product_id = fields.Many2one('product.product', 'Product Variant',)
    lot_id = fields.Many2one('stock.production.lot','lot')
    move_id = fields.Many2one('stock.move','Move')
    move_line_id = fields.Many2one('stock.move.line','Move Line')
    product_produce_id = fields.Integer('Product Produce')
    product_produce_line_id = fields.Integer('Product Produce Line')
    qty_done = fields.Float(string="quantity")
    consumed_weight = fields.Float('Consumed Weight', store=True, digits=dp.get_precision('Stock Weight'), help="Weight consumed", oldname='total_weight')
    finished_product_id = fields.Many2one('product.product', 'Finish Product',)
    finished_lot_id = fields.Many2one('stock.production.lot','Finish Lot')
    finished_qty_done = fields.Float(string="Finish quantity")
    finished_produced_weight = fields.Float('Produced Weight', store=True, digits=dp.get_precision('Stock Weight'), help="Produced Weight")