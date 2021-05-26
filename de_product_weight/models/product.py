# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    weight_available = fields.Float(compute='_compute_total_weight', string='Weight Available', readonly=True, store=True)
    #weight_available = fields.Float(string='Weight Available')
    is_weight_uom = fields.Boolean('Weight UOM',default=True)
    weight_done = fields.Float('Weight Done')
    
    @api.depends(
		'product_variant_ids',
		#'product_variant_ids.stock_move_ids.product_qty',
		#'product_variant_ids.stock_move_ids.state',
	)
    #@api.depends_context('company_owned', 'force_company')
    def _compute_total_weight(self):
        """
        Compute the total weight of physical storeage locations
        """
		#product_ids = self.env['product.product'].search([('product_tmpl_id', '=', rs.id)])
		#move_lines = self.env['stock.move.line'].search([('product_id', '=', product_id.id)])
        total_weight = 0
        for product in self.product_variant_ids:
            total_weight += product.weight_available
        self.weight_available = total_weight
        
    def action_update_weight_stock(self):
        lots = self.env['stock.production.lot']
        for product in self.product_variant_ids:
            total_weight = update_total_weight = 0
            #wegiht_move_lines = self.env['stock.move.line'].search([('product_id', '=', product.id),])
            product_moves = self.env['stock.move'].search([('product_id', '=', product.id),])
            for mv in product_moves:
                update_total_weight = 0
                for line in mv.move_line_ids:
                    if line.total_weight <=0:
                        line.total_weight = line.qty_done * line.product_id.weight
                        update_total_weight += line.qty_done * line.product_id.weight
                    else:
                        update_total_weight += line.total_weight
                mv.total_weight = update_total_weight
                            
            lots = self.env['stock.production.lot'].search([('product_id', '=', product.id)])
            if lots:
                for lot in lots:
                    lot_weight =0
                    move_lines = self.env['stock.move.line'].search([('product_id', '=', product.id),('lot_id', '=', lot.id)])
                            
                    for line in move_lines.filtered(lambda x: x.move_id.state in ('done')):
                        if line.total_weight <=0:
                            line.write({
                                'total_weight':line.qty_done * product.weight
                            })
                        if line.location_id.usage == 'internal':
                            if lot.product_weight > 0:
                                lot_weight -= line.total_weight
                                total_weight -= line.total_weight 
                            else:
                                lot_weight -= line.qty_done * product.weight
                                total_weight -= line.total_weight 
                        elif line.location_dest_id.usage == 'internal':
                            if lot.product_weight > 0:
                                lot_weight += line.total_weight
                                total_weight += line.total_weight 
                            else:
                                lot_weight += line.qty_done * product.weight
                                total_weight += line.total_weight
                            
                           
                    lot.write({
                        'product_weight': lot_weight
                    })
            product.weight_available = total_weight
            self._compute_total_weight()
                
                
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    weight_available = fields.Float(string='Weight Available')