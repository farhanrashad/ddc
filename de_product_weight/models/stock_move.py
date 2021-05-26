# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from psycopg2 import OperationalError, Error

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

import logging

_logger = logging.getLogger(__name__)

from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    total_weight = fields.Float('Total Weight', store=False, digits=dp.get_precision('Stock Weight'), compute='_calculate_total_weight', readonly=True)
            
    @api.depends('move_line_ids','move_line_nosuggest_ids','product_id')
    def _calculate_total_weight(self):
        for line in self:
            sum_weight = sum_weight1 = 0
            for move_line in line.move_line_ids:
                if not move_line.total_weight:
                    sum_weight += move_line.qty_done * move_line.weight
                else:
                    sum_weight += move_line.total_weight
            line.total_weight = sum_weight
			
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), readonly=False, help="Weight of the product in order line")
    
    #@api.depends('product_id','lot_id','qty_done', 'weight')
    #def _calculate_total_weight(self):
        #for line in self:
            #if line.total_weight == 0 or not line.total_weight:
                #line.total_weight = line.qty_done * line.weight
            
    @api.onchange('product_id','lot_id')
    def onchange_product(self):
        if self.lot_id:
            self.qty_done = self.lot_id.product_qty
    
    def write(self, vals):
        res = super(StockMoveLine, self).write(vals)
        for ml in self:
            self._update_product_weight(ml.product_id.id,ml.location_id.id,ml.total_weight*-1, ml.lot_id.id, ml.package_id.id, ml.owner_id.id, ml.date)
            self._update_product_weight(ml.product_id.id,ml.location_dest_id.id,ml.total_weight, ml.lot_id.id, ml.package_id.id, ml.owner_id.id, ml.date)
        return res
    
    #@api.model
    def _update_product_weight(self, product_id, location_id, weight, lot_id=None, package_id=None, owner_id=None, in_date=None):
        self = self.sudo()
        lot = self.env['stock.production.lot'].search([('id','=',lot_id)])
        lot.update({
            'product_weight': lot.product_weight + weight
        })
        query = query_params = ''
        
        if lot_id:
            query_params = query_params + ' and lot_id = ' + str(lot_id)
            
        if package_id:
            query_params = query_params + ' and package_id = ' + str(package_id)
            
        if owner_id:
            query_params = query_params + ' and owner_id = ' + str(owner_id)
            
        params = {'product_id': product_id, 'weight':weight,'location_id': location_id, 'lot_id': lot_id}
        
        if lot_id: 
            query = """
        update stock_quant set product_weight = product_weight + %(weight)s where lot_id = %(lot_id)s and location_id = %(location_id)s 
        """ 
            self.env.cr.execute(query, params=params)
        
        
        
        #self._cr.execute("update stock_quant set product_weight=15")
        #.search([('product_id','=',product_id),('location_id','=',location_id),('lot_id','=',lot_id),])
        #quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=True)