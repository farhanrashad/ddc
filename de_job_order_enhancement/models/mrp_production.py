# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp
import threading


# class MRPProductProduce(models.TransientModel):
#     _inherit = 'mrp.product.produce'
    
    
#     @api.model
#     def default_get(self, fields):
#         res = super(MRPProductProduce, self).default_get(fields)
#         production = self.env['mrp.production']
#         production_id = self.env.context.get('default_production_id') or self.env.context.get('active_id')
#         if production_id:
#             production = self.env['mrp.production'].browse(production_id)
#             raw_workorder_ids = []
#             for move_line in production.move_raw_ids:
#                 raw_workorder_ids.append(0,0,{
#                       'product_id':  move_line.product_id.id,
#                       'qty_to_consume': move_line.product_uom_qty,
#                       'produced_weight': move_line.total_weight,
#                 })
                
#         if production.exists():
#             serial_finished = (production.product_id.tracking == 'serial')
#             todo_uom = production.product_uom_id.id
#             todo_quantity = self._get_todo(production)
#             if serial_finished:
#                 todo_quantity = 1.0
#                 if production.product_uom_id.uom_type != 'reference':
#                     todo_uom = self.env['uom.uom'].search([('category_id', '=', production.product_uom_id.category_id.id), ('uom_type', '=', 'reference')]).id
#             if 'production_id' in fields:
#                 res['production_id'] = production.id
#             if 'product_id' in fields:
#                 res['product_id'] = production.product_id.id
#             if 'product_uom_id' in fields:
#                 res['product_uom_id'] = todo_uom
#             if 'produced_weight' in fields:
#                 res['produced_weight'] = production.production_weight   
#             if 'serial' in fields:
#                 res['serial'] = bool(serial_finished)
#             if 'qty_producing' in fields:
#                 res['qty_producing'] = todo_quantity
#             if 'consumption' in fields:
#                 res['consumption'] = production.bom_id.consumption
#         return res

    
#     produced_weight = fields.Float('Weight Produced', digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
  
        



class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    production_total_weight = fields.Float(string='Production Weight')
    
    


