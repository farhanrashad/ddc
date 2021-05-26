# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp
import threading




class JobOrder(models.Model):
    _inherit = 'job.order'
    
    def action_material_planning(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
#             'multi': False,
            'name': 'Material Planning',
            'domain': [('job_order_id','=', self.id)],
            'target': 'current',
            'res_model': 'job.order.bom.component',
            'view_mode': 'tree,form',
        }
    
    def action_confirm(self):
        res = super(JobOrder, self).action_confirm()
        for line in self.sale_id.order_line:
            for order_line in self.job_order_sale_lines:

                if order_line.product_id.id == line.product_id.id:
                    order_line.update({
                        'unit_weight': line.weight,
                    })
        return res
    
    
    
    
    
    
    

    
    
    job_order_material_ids = fields.One2many('job.order.bom.component', 'job_order_id', string='Job Order MRP Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)

    
    
    def action_process(self):
        res = super(JobOrder, self).action_process()
        product_list = []
        bom_product = []
        all_boms = []
        for sale in self.job_order_sale_lines:
            sale_product = sale.product_id.id
            order_qty = sale.product_uom_qty
            unit_weight = sale.unit_weight
            bom_versions = sale.bom_version
            
            velour_greige_qty = 0.0                
            for rule in self.struct_id.rule_ids:
                if rule.code=='VW':
                    velour_greige_qty = (1 + (rule.quantity_percentage/100))
                    
            sized_yarn_qty = 0.0                
            for rule in self.struct_id.rule_ids:
                if rule.code=='CDW':
                    sized_yarn_qty = (1 + (rule.quantity_percentage/100))        
                
            yarn_qty = 0.0                
            for rule in self.struct_id.rule_ids:
                if rule.code=='HWP':
                    yarn_qty = (1 + (rule.quantity_percentage/100))
                
            greige_qty = 0.0                
            for rule in self.struct_id.rule_ids:
                if rule.code=='DWP':
                    greige_qty = 1 + (rule.quantity_percentage/100)
                    
            product_variant_bom = self.env['mrp.bom'].search([('product_id','=',sale.product_id.id)])
            product_tmpl_bom = self.env['mrp.bom'].search([('product_tmpl_id.name','=',sale.product_id.name)])
                
       # SO  product bom
            variant_qty = 0.0                
            for rule in self.struct_id.rule_ids:
                if rule.code=='BGP':
                    variant_qty = 1 + (rule.quantity_percentage/100)
                    
            if product_variant_bom:
                variant_bom_category0 = product_variant_bom.product_id.categ_id.id 
                bom_vals =   {
                         'job_order_id':  self.name,
                         'product_id': product_variant_bom.product_id.id,
                         'type': product_variant_bom.type,
                         'quantity':  product_variant_bom.product_qty,
                         'production_quantity': order_qty * variant_qty,
                         'weight':  unit_weight * order_qty * variant_qty,
                         'source_product_id': sale_product,
                           }  
                bom_product.append(bom_vals)
                for component_level1 in product_variant_bom[0].bom_line_ids:   
            # Level 1 

                    component_categ1 = component_level1.product_id.categ_id.id
                    product_list.append(component_level1.product_id.name)
                    component_bom_level1_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level1.product_id.name)])
                    component_production_quantity1 = 0
                    component_weight1 = 0
                    if component_bom_level1_type.categ_id.id == 10:
                        component_production_quantity1 =  order_qty * variant_qty
                        component_weight1 = unit_weight * order_qty * variant_qty
                    elif component_bom_level1_type.categ_id.id == 12:
                        component_production_quantity1 =  order_qty * variant_qty
                        component_weight1 = unit_weight * order_qty * variant_qty    
                    elif component_bom_level1_type.categ_id.id == 15:
                        component_production_quantity1 =  order_qty * variant_qty
                        component_weight1 = unit_weight * order_qty * variant_qty 
                    elif component_bom_level1_type.categ_id.id == 22:
                        component_production_quantity1 =  order_qty * variant_qty
                        component_weight1 = unit_weight * order_qty * variant_qty
                       
                    elif component_level1.product_id.categ_id.id == 14 or component_level1.product_id.categ_id.id == 17:
                        component_production_quantity1 =  (component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                        component_weight1 = component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty

                    elif component_level1.product_id.categ_id.id == 22 or component_level1.product_id.categ_id.id == 13:
                        component_production_quantity1 =  (component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                        component_weight1 = component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty    
                         
                        
                    elif component_level1.product_id.categ_id.id == 16:
                        component_production_quantity1 =  (component_level1.product_qty * order_qty * variant_qty)
                        component_weight1 = component_level1.product_qty * unit_weight * order_qty * variant_qty
                            
                    if component_bom_level1_type:    
                        bom_vals =   {
                                 'job_order_id':  self.name,
                                 'product_id': component_level1.product_id.id,
                                 'type': component_bom_level1_type[0].type,
                                 'quantity':  component_level1.product_qty,
                                 'production_quantity': component_production_quantity1,
                                 'weight':  component_weight1,
                                 'source_product_id': sale_product,
                                       }  
                        bom_product.append(bom_vals)
                    else:
                        bom_vals =   {
                                 'job_order_id':  self.name,
                                 'product_id': component_level1.product_id.id,
                                 'type': component_bom_level1_type.type,
                                 'quantity':  component_level1.product_qty,
                                 'production_quantity': component_production_quantity1,
                                 'weight':  component_weight1,
                                 'source_product_id': sale_product,
                                       }  
                        bom_product.append(bom_vals)
                        
                    
                    component_bom_level2 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level1.product_id.name)])
             # Level 2 
                    component_production_quantity2 = 0
                    component_weight2 = 0
                    if component_bom_level2:
                        for component_level2 in component_bom_level2[0].bom_line_ids:
                            
                            product_list.append(component_level2.product_id.name)
                            component_bom_level2_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level2.product_id.name)])
                            if component_bom_level2_type.categ_id.id == 10:
                                component_production_quantity2 =  order_qty * variant_qty
                                component_weight2 = unit_weight * order_qty * variant_qty * greige_qty
                            elif component_bom_level2_type.categ_id.id == 12:
                                component_production_quantity2 =  order_qty * variant_qty
                                component_weight2 = unit_weight * order_qty * variant_qty * greige_qty
                            elif component_level2.product_id.categ_id.id == 27:
                                component_production_quantity2 =  order_qty * variant_qty
                                component_weight2 = unit_weight * order_qty * variant_qty * greige_qty    
                            elif component_level2.product_id.categ_id.id == 14 and  variant_bom_category0 != 12:
                                component_production_quantity2 =  (component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty 

                            elif component_level2.product_id.categ_id.id == 17 and  variant_bom_category0 != 12:
                                component_production_quantity2 =  (component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty 

                            elif component_level2.product_id.categ_id.id == 22 and  variant_bom_category0 != 12:
                                component_production_quantity2 =  (component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty 

                            elif component_level2.product_id.categ_id.id == 13 and  variant_bom_category0 != 12:
                                component_production_quantity2 =  (component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty 

                            elif component_level2.product_id.categ_id.id == 17 and  component_categ1 == 14:
                                component_production_quantity2 =  (component_level2.product_qty *  unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty *  unit_weight * order_qty * variant_qty 

                            elif component_level2.product_id.categ_id.id == 22 and  component_categ1 == 14:
                                component_production_quantity2 =  (component_level2.product_qty *  unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty *  unit_weight * order_qty * variant_qty
 
                            elif component_level2.product_id.categ_id.id == 13 and  component_categ1 == 14:
                                component_production_quantity2 =  (component_level2.product_qty *  unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty *  unit_weight * order_qty * variant_qty 


                             
                                
                            elif component_level2.product_id.categ_id.id == 17:
                                component_production_quantity2 =  (component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty)/component_level1.product_id.uom_po_id.factor_inv
                                component_weight2 = component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty 
                            elif component_level2.product_id.categ_id.id == 14 and variant_bom_category0 == 12:
                                component_production_quantity2 =  (component_level2.product_qty * component_production_quantity1 * sized_yarn_qty )
                                component_weight2 = component_level2.product_qty * component_weight1 * sized_yarn_qty    

                            if component_bom_level2_type:    
                                
                                bom_vals =   {
                                     'job_order_id':  self.name,
                                     'product_id': component_level2.product_id.id,
                                     'type': component_bom_level2_type[0].type,
                                     'quantity':  component_level2.product_qty,
                                     'production_quantity': component_production_quantity2,
                                     'weight':   component_weight2,
                                     'source_product_id': sale_product,
                                       }  
                                bom_product.append(bom_vals)
                            else:
                                bom_vals =   {
                                     'job_order_id':  self.name,
                                     'product_id': component_level2.product_id.id,
                                     'type': component_bom_level2_type.type,
                                     'quantity':  component_level2.product_qty,
                                     'production_quantity': component_production_quantity2,
                                     'weight':   component_weight2,
                                     'source_product_id': sale_product,
                                       }  
                                bom_product.append(bom_vals)
                                


                            component_bom_level3 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level2.product_id.name)])
             # Level 3 
#======================================           ============================================
             # Greige BOM  
                            component_production_quantity3 = 0
                            component_weight3 = 0
                            component_categ3 = 0
                            if component_bom_level3: 
                                for component_level3 in component_bom_level3[bom_versions].bom_line_ids:
                                    component_categ3 = component_level3.product_id.categ_id.id
                                    
                                    product_list.append(component_level3.product_id.name)
                                    component_bom_level3_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level3.product_id.name)])
                                    
                                    if component_level3.product_id.categ_id.id == 14:
                                        component_production_quantity3 =  (component_level3.product_qty * yarn_qty * component_production_quantity2)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weight3 = component_level3.product_qty * yarn_qty * component_weight2
                                    elif component_level3.product_id.categ_id.id == 22:
                                        component_production_quantity3 =  (component_level3.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weight3 = component_level3.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty
                           
                                    elif component_level3.product_id.categ_id.id == 13:
                                        component_production_quantity3 =  (component_level3.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weight3 = component_level3.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty 
   
                                    elif  component_level3.product_id.categ_id.id == 17:
                                        component_production_quantityt3 =  (component_level3.product_qty * yarn_qty * component_production_quantity2)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weight3 = component_level3.product_qty * yarn_qty * component_weight2                          
#                                         raise UserError(_(''+ str(component_weight3)))
                                    elif component_level3.product_id.categ_id.id == 12:
                                        component_production_quantity3 =   (order_qty * variant_qty)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weight3 = unit_weight * order_qty * variant_qty * greige_qty * velour_greige_qty
                                    
                                    elif component_level3.product_id.categ_id.id == 16:
                                        component_production_quantity3 =  (component_level3.product_qty * order_qty * variant_qty)
                                        component_weight3 = component_level3.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty                                         
                                        component_categ3 =  component_level3.product_id.categ_id.id
                                    else:
                                        component_production_quantityt3 =  (component_level3.product_qty * yarn_qty * component_production_quantity2)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weightt3 = component_level3.product_qty * yarn_qty * component_weight2 

                                    bom_vals =   {
                                         'job_order_id':  self.name,
                                         'product_id': component_level3.product_id.id,
                                         'type': component_bom_level3_type.type,
                                         'quantity':  component_level3.product_qty,
                                         'production_quantity': component_production_quantity3,
                                         'weight': component_weight3,
                                         'source_product_id': sale_product,
                                           }  
                                    bom_product.append(bom_vals)


                                    component_bom_level4 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level3.product_id.name)])
                             # Level 4       
                                    if component_bom_level4:
                                        for component_level4 in component_bom_level4.bom_line_ids:
                                            product_list.append(component_level4.product_id.name)

                                            component_bom_level4_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level4.product_id.name)])
                                            if component_level4.product_id.categ_id.id == 12:
                                                component_production_quantity4 =   (component_level4.product_qty * order_qty * variant_qty * velour_greige_qty * yarn_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * unit_weight * order_qty * variant_qty * greige_qty * velour_greige_qty * yarn_qty
                                            elif component_categ3 != 16 and component_level4.product_id.categ_id.id == 14:
                                                component_production_quantity4 =  (component_level4.product_qty * order_qty * variant_qty * yarn_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty * yarn_qty 

                                            elif component_categ3 != 16 and component_level4.product_id.categ_id.id == 17:
                                                component_production_quantity4 =  (component_level4.product_qty * order_qty * variant_qty * yarn_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty * yarn_qty

                                            elif component_categ3 != 16 and component_level4.product_id.categ_id.id == 22:
                                                component_production_quantity4 =  (component_level4.product_qty * component_production_quantity3)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * component_weight3  

                                            elif component_categ3 != 16 and component_level4.product_id.categ_id.id == 13:
                                                component_production_quantity4 =  (component_level4.product_qty * order_qty * variant_qty * yarn_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty * yarn_qty

                                            elif component_categ3 == 14 and component_level4.product_id.categ_id.id == 13:
                                                component_production_quantity4 =  (component_level4.product_qty * order_qty * variant_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty 

                                            elif component_categ3 == 14 and component_level4.product_id.categ_id.id == 17:
                                                component_production_quantity4 =  (component_level4.product_qty * order_qty * variant_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty  

                                            elif component_categ3 == 14 and component_level4.product_id.categ_id.id == 22:

                                                component_production_quantity4 =  (component_level4.product_qty * order_qty * variant_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty  
                                                
                                            elif component_level4.product_id.categ_id.id == 14 and component_categ3 == 16:
                                                component_production_quantity4 =  (component_level4.product_qty * component_production_quantity3 * sized_yarn_qty )
                                                component_weight4 = component_level4.product_qty * component_weight3 * sized_yarn_qty

                                            elif component_level4.product_id.categ_id.id == 22 and component_categ3 == 16:
                                                component_production_quantity4 =  (component_level4.product_qty * component_production_quantity3 * sized_yarn_qty )
                                                component_weight4 = component_level4.product_qty * component_weight3 * sized_yarn_qty 

                                            elif component_level4.product_id.categ_id.id == 13 and component_categ3 == 16:
                                                component_production_quantity4 =  (component_level4.product_qty * component_production_quantity3 * sized_yarn_qty )
                                                component_weight4 = component_level4.product_qty * component_weight3 * sized_yarn_qty

                                            elif component_level4.product_id.categ_id.id == 17 and component_categ3 == 16:
                                                component_production_quantity4 =  (component_level4.product_qty * component_production_quantity3 * sized_yarn_qty )
                                                component_weight4 = component_level4.product_qty * component_weight3 * sized_yarn_qty

                                                
                                                
                                            else:
                                                component_production_quantity4 =   (component_level4.product_qty * yarn_qty *unit_weight * order_qty * variant_qty * greige_qty)/component_level4.product_id.uom_po_id.factor_inv
                                                component_weight4 = component_level4.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty                                  
                                            

                                            bom_vals =   {
                                                 'job_order_id':  self.name,
                                                 'product_id': component_level4.product_id.id,
                                                 'type': component_bom_level4_type.type,
                                                 'quantity':  component_level4.product_qty,
                                                 'production_quantity':  component_production_quantity4,
                                                'weight': component_weight4 ,
                                                 'source_product_id': sale_product,
                                               }  
                                            bom_product.append(bom_vals) 

                             # Level 5       
                                            component_bom_level5 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level4.product_id.name)])
                                        
                                            if component_bom_level5:
                                                for component_level5 in component_bom_level5.bom_line_ids:
                                                    product_list.append(component_level5.product_id.name)
                                                    component_bom_level5_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level5.product_id.name)])
                                                    
                                                    if component_level5.product_id.categ_id.id == 17:
                                                        component_production_quantity5 =   (component_level5.product_qty * component_production_quantity4)/component_level5.product_id.uom_po_id.factor_inv
                                                        component_weight5 = component_level5.product_qty * component_weight4


                                                    bom_vals =   {
                                                         'job_order_id':  self.name,
                                                         'product_id': component_level5.product_id.id,
                                                         'type': component_bom_level5_type.type,
                                                         'quantity':  component_level5.product_qty,
                                                         'production_quantity': component_production_quantity5,
                                                         'weight':component_weight5,
                                                         'source_product_id': sale_product,

                                                           }  
                                                    bom_product.append(bom_vals) 

                               # Level 6       
                                                    component_bom_level6 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level5.product_id.name)])
                                                  
                                                    if component_bom_level6:
                                                        for component_level6 in component_bom_level6.bom_line_ids:
                                                            product_list.append(component_level6.product_id.name)
                                                            component_bom_level6_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level6.product_id.name)])
                                                            bom_vals =   {
                                                                 'job_order_id':  self.name,
                                                                 'product_id': component_level6.product_id.id,
                                                                 'type': component_bom_level6_type.type,
                                                                 'quantity':  component_level6.product_qty,
                                                                 'production_quantity':  (component_level4.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level4.product_id.uom_po_id.factor_inv,
                                                                 'weight':component_level4.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty,
                                                                 'source_product_id': sale_product,
                                                             }  
                                                            bom_product.append(bom_vals)

                                    # Level 7       
                                                            component_bom_level7 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level6.product_id.name)])
                                                          
                                                            if component_bom_level7:
                                                                for component_level7 in component_bom_level7.bom_line_ids:
                                                                    product_list.append(component_level7.product_id.name)
                                                                    component_bom_level7_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level7.product_id.name)])
                                                                    bom_vals =   {
                                                                        'job_order_id':  self.name,
                                                                        'product_id': component_level7.product_id.id,
                                                                        'type': component_bom_level7_type.type,
                                                                        'quantity':  component_level7.product_qty,
                                                                        'source_product_id': sale_product,
                                                                           }  
                                                                    bom_product.append(bom_vals)

                                                                    
                                                                
            else:
                bom_vals =   {
                         'job_order_id':  self.name,
                         'product_id': sale_product,
                         'type': product_tmpl_bom.type,
                         'quantity':  product_tmpl_bom.product_qty,
                         'production_quantity': order_qty * variant_qty,
                         'weight':  unit_weight * order_qty * variant_qty,
                         'source_product_id': sale_product,
                           }  
                bom_product.append(bom_vals)
                for component_level1 in product_tmpl_bom[0].bom_line_ids:   
            # Level 1
                    component_production_quantityt1 = 0
                    component_weightt1 = 0
                    product_list.append(component_level1.product_id.name)
                    component_bom_level1_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level1.product_id.name)])
                    if component_level1.product_id.categ_id.id == 10 :
                        component_production_quantityt1 =  order_qty * variant_qty
                        component_weightt1 = unit_weight * order_qty * variant_qty
                    elif component_level1.product_id.categ_id.id == 12:
                        component_production_quantityt1 =  order_qty * variant_qty
                        component_weightt1 = unit_weight * order_qty * variant_qty 
                    elif component_level1.product_id.categ_id.id == 14 :
                        component_production_quantityt1 =  (component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level1.product_id.uom_po_id.factor_inv
                        component_weightt1 = component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty
                    elif component_level1.product_id.categ_id.id == 17:
                        component_production_quantityt1 =  (component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level1.product_id.uom_po_id.factor_inv
                        component_weightt1 = component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty
                        
                    elif component_level1.product_id.categ_id.id == 13:
                        component_production_quantityt1 =  (component_level1.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty)/component_level1.product_id.uom_po_id.factor_inv
                        component_weightt1 = component_level1.product_qty * unit_weight * yarn_qty * order_qty * variant_qty * greige_qty * sized_yarn_qty   
                    if component_bom_level1_type:    
                        bom_vals =   {
                                 'job_order_id':  self.name,
                                 'product_id': component_level1.product_id.id,
                                 'type': component_bom_level1_type[0].type,
                                 'quantity':  component_level1.product_qty,
                                 'production_quantity': component_production_quantityt1,
                                 'weight':  component_weightt1,
                                 'source_product_id': sale_product,
                                       }  
                        bom_product.append(bom_vals)
                    else:
                        bom_vals =   {
                                 'job_order_id':  self.name,
                                 'product_id': component_level1.product_id.id,
                                 'type': component_bom_level1_type.type,
                                 'quantity':  component_level1.product_qty,
                                 'production_quantity': component_production_quantityt1,
                                 'weight':  component_weightt1,
                                 'source_product_id': sale_product,
                                       }  
                        bom_product.append(bom_vals)
                        

                    component_bom_level2 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level1.product_id.name)])
             # Level 2  
                    component_production_quantityt2 = 0
                    component_weightt2 = 0 
                    if component_bom_level2:
                        for component_level2 in component_bom_level2[0].bom_line_ids:
                            product_list.append(component_level2.product_id.name)
                            component_bom_level2_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level2.product_id.name)])
                            if component_level2.product_id.categ_id.id == 13:
                                component_production_quantityt2 =  (component_level2.product_qty * order_qty * variant_qty * yarn_qty)/component_level2.product_id.uom_po_id.factor_inv
                                component_weightt2 = component_level2.product_qty * order_qty * variant_qty * yarn_qty
                            elif component_level2.product_id.categ_id.id == 12:
                                component_production_quantityt2 =  order_qty * variant_qty
                                component_weightt2 = unit_weight * order_qty * variant_qty * greige_qty
                            elif component_level2.product_id.categ_id.id == 14 :
                                component_production_quantityt2 =  (component_level2.product_qty * order_qty * variant_qty * yarn_qty)/component_level2.product_id.uom_po_id.factor_inv
                                component_weightt2 = component_level2.product_qty *order_qty * variant_qty * yarn_qty
                                
                            elif  component_level2.product_id.categ_id.id == 17:
                                component_production_quantityt2 =  (component_level2.product_qty * order_qty * variant_qty * yarn_qty)/component_level2.product_id.uom_po_id.factor_inv
                                component_weightt2 = component_level2.product_qty *order_qty * variant_qty * yarn_qty
                                       
                            elif component_level2.product_id.categ_id.id == 17:
                                component_production_quantityt2 =  (component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level2.product_id.uom_po_id.factor_inv
                                component_weightt2 = component_level2.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty    
                            
                            bom_vals =   {
                                 'job_order_id':  self.name,
                                 'product_id': component_level2.product_id.id,
                                 'type': component_bom_level2_type.type,
                                 'quantity':  component_level2.product_qty,
                                 'production_quantity':  component_production_quantityt2,
                                 'weight': component_weightt2,
                                 'source_product_id': sale_product,
                                   }  
                            bom_product.append(bom_vals)


                            component_bom_level3 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level2.product_id.name)])
             # Level 3       
                            component_production_quantityt3 = 0
                            component_weightt3 = 0
                            if component_bom_level3:
                                for component_level3 in component_bom_level3[bom_versions].bom_line_ids:
                                    product_list.append(component_level3.product_id.name)
                                    component_bom_level3_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level3.product_id.name)])
                                    if component_level3.product_id.categ_id.id == 14 :
                                        component_production_quantityt3 =  (component_level3.product_qty * order_qty * variant_qty * yarn_qty * sized_yarn_qty)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weightt3 = component_level2.product_qty * order_qty * variant_qty * yarn_qty * sized_yarn_qty
                                        
                                    elif component_level3.product_id.categ_id.id == 17:
                                        component_production_quantityt3 =  (component_level3.product_qty * order_qty * variant_qty * yarn_qty * sized_yarn_qty)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weightt3 = component_level2.product_qty * order_qty * variant_qty * yarn_qty * sized_yarn_qty
                                        
                                        
                                    elif component_level3.product_id.categ_id.id == 13:
                                        component_production_quantityt3 =   (component_level3.product_qty * unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty)/component_level3.product_id.uom_po_id.factor_inv
                                        component_weightt3 = component_level3.product_qty *  unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty   
                                    bom_vals =   {
                                         'job_order_id':  self.name,
                                         'product_id': component_level3.product_id.id,
                                         'type': component_bom_level3_type.type,
                                         'quantity':  component_level3.product_qty,
                                         'production_quantity':  component_production_quantityt3,
                                         'weight': component_weightt3,
                                         'source_product_id': sale_product,
                                           }  
                                    bom_product.append(bom_vals)


                                    component_bom_level4 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level3.product_id.name)])
                             # Level 4       

                                    if component_bom_level4:
                                        for component_level4 in component_bom_level4.bom_line_ids:
                                            product_list.append(component_level4.product_id.name)

                                            component_bom_level4_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level4.product_id.name)])


                                            bom_vals =   {
                                                 'job_order_id':  self.name,
                                                 'product_id': component_level4.product_id.id,
                                                 'type': component_bom_level4_type.type,
                                                 'quantity':  component_level4.product_qty,
                                                 'production_quantity':  (component_level4.product_qty * component_level3.product_qty * yarn_qty *  unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty)/component_level4.product_id.uom_po_id.factor_inv,
                                                'weight':component_level4.product_qty * component_level3.product_qty * yarn_qty *  unit_weight * order_qty * variant_qty * greige_qty * sized_yarn_qty,
                                                 'source_product_id': sale_product,
                                               }  
                                            bom_product.append(bom_vals) 

                             # Level 5       
                                            component_bom_level5 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level4.product_id.name)])
                                            if component_bom_level5:
                                                for component_level5 in component_bom_level5.bom_line_ids:
                                                    product_list.append(component_level5.product_id.name)
                                                    component_bom_level5_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level5.product_id.name)])


                                                    bom_vals =   {
                                                         'job_order_id':  self.name,
                                                         'product_id': component_level5.product_id.id,
                                                         'type': component_bom_level5_type.type,
                                                         'quantity':  component_level5.product_qty,
                                                         'production_quantity':  (component_level4.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level4.product_id.uom_po_id.factor_inv,
                                                'weight':component_level4.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty,
                                                         'source_product_id': sale_product,

                                                           }  
                                                    bom_product.append(bom_vals) 

                               # Level 6       
                                                    component_bom_level6 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level5.product_id.name)])
                                                    if component_bom_level6:
                                                        for component_level6 in component_bom_level6.bom_line_ids:
                                                            product_list.append(component_level6.product_id.name)
                                                            component_bom_level6_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level6.product_id.name)])
                                                            bom_vals =   {
                                                                 'job_order_id':  self.name,
                                                                 'product_id': component_level6.product_id.id,
                                                                 'type': component_bom_level6_type.type,
                                                                 'quantity':  component_level6.product_qty,
                                                                 'production_quantity':  (component_level4.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty)/component_level4.product_id.uom_po_id.factor_inv,
                                                                 'weight':component_level4.product_qty * yarn_qty * unit_weight * order_qty * variant_qty * greige_qty,
                                                                 'source_product_id': sale_product,
                                                             }  
                                                            bom_product.append(bom_vals)

                                    # Level 7       
                                                            component_bom_level7 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level6.product_id.name)])
                                                            if component_bom_level7:
                                                                for component_level7 in component_bom_level7.bom_line_ids:
                                                                    product_list.append(component_level7.product_id.name)
                                                                    component_bom_level7_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level7.product_id.name)])
                                                                    bom_vals =   {
                                                                        'job_order_id':  self.name,
                                                                        'product_id': component_level7.product_id.id,
                                                                        'type': component_bom_level7_type.type,
                                                                        'quantity':  component_level7.product_qty,
                                                                        'source_product_id': sale_product,
                                                                           }  
                                                                    bom_product.append(bom_vals)
                

            
        for product in bom_product:
                    
            all_boms.append((0,0,{
                            'job_order_id':  product['job_order_id'],
                            'product_id': product['product_id'],
                            'type': product['type'],
                            'quantity': product['quantity'],
                            'weight': product['weight'],
                            'production_quantity': product['production_quantity'],  
                            'source_product_id': product['source_product_id']
                            })) 
            
        self.job_order_material_ids = all_boms             
        for product in self.job_order_material_ids:
            line_product = []
            product_values = self.env['product.product'].search([('id','=',product.product_id.id)])
            for vendor in product_values.seller_ids:
                line_product.append(vendor.name.id)
            if product.type != 'normal':
                if line_product == []:
                    raise UserError(_('Please Select Vendor on Product Form:' + ' ' + str(product.product_id.name)))
                product.update({
                       'vendor_id': line_product[0],
                   }) 
                
        return res

    

    
class JobOrderLine(models.Model):
    _inherit = 'job.order.sale.line'
    
    
    unit_weight = fields.Float(string='Unit Weight')
    bom_ids = fields.Many2one('mrp.bom', string="Greige BOM")
    bom_version = fields.Integer(string="BOM Version", default=0)
    greige_bom_ids = fields.Many2many('mrp.bom', string="Greige BOM")
    
    
    
    
class JobOrderBOMCompoent(models.Model):
    _name = 'job.order.bom.component'
    _description = 'Jor Order Production'
    
    def _default_picking_type(self):
        return self.env['stock.picking.type'].search([
            ('code', '=', 'mrp_operation'),],
            limit=1).id
    
    def _default_src_location(self):
        return self.env['stock.location'].search([
             ('name', '=', 'Stock'),],
            limit=1).id
    
    def _default_dest_location(self):
        return self.env['stock.location'].search([
            ('name', '=', 'Stock'),],
            limit=1).id
    
    def _default_company(self):
        return self.env['res.company'].search([
            ('name', '=', 'Al-Ghani International'),],
            limit=1).id
    
    def unlink(self):
        for leave in self:
            if leave.po_created == True   or leave.po_created == False:
                raise UserError(_('You cannot delete an order'))
     
            return super(JobOrderBOMCompoent, self).unlink()
    
    
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', string='Vendor', index=True)
    po_created = fields.Boolean(string="PO Created")
    is_duplicate = fields.Boolean(string="Is Duplicate")
    production_created = fields.Boolean(string="MO Created")
    product_id = fields.Many2one('product.product', string='Product',readonly=True)
    category_id = fields.Many2one(related='product_id.categ_id')
    source_product_id = fields.Many2one('product.product', string='Source Product',readonly=True)
    weight = fields.Float(string='Weight',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit'),
        ('subcontract', 'Subcontracting')
          ], 'BoM Type',
        default='normal')
    quantity = fields.Float(string='BOM Quantity',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    production_quantity = fields.Float(string='Production Quantity')
    company_id = fields.Many2one('res.company', store=True, string='Company', readonly=False, default=_default_company,)
    location_src_id = fields.Many2one('stock.location', 'From', check_company=True, default=_default_src_location,)
    location_dest_id = fields.Many2one('stock.location', 'To', check_company=True, default=_default_dest_location,)
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
         readonly=True, default=_default_picking_type,)
    


    
    
    
    def _calcualte_production_quantity(self):
        self.production_quantity = 0  
        
        
    def action_generate_production_order(self):
        product_uniq_list = []
        count = 0
        for line in self:
            job_order_ids = line.job_order_id.id
            production_qty = 0.0
            production_weight = 0.0
            product_count = 0
            if line.production_created == False and line.type == 'normal':
                if line.is_duplicate == True:   
                    product_uniq_list.append(line.product_id.id)        
                line__bom_vals = []        
                bom_qty = 0.0
                line_bom = self.env['mrp.bom'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id)])
                variant_line_bom = self.env['mrp.bom'].search([('product_id','=',line.product_id.id)])
#                 raise UserError((str(line.product_id.id)))
                if variant_line_bom:
                    for bom in variant_line_bom[0]:
                        for component in bom.bom_line_ids:
                        
                            product1_weight1 = self.env['job.order.bom.component'].search([('product_id','=',component.product_id.id),('job_order_id','=', line.job_order_id.id)])
                            line__bom_vals.append((0,0, {
                                    'product_id': component.product_id.id,
                                    'name': component.product_id.name,
                                    'product_uom': component.product_id.uom_id.id,
                                    'product_uom_qty':product1_weight1.production_quantity,
                                    'stock_total_weight': product1_weight1.weight, 
                                    'date': fields.Date.today(),
                                    'date_expected': fields.Date.today(),
                                    'location_id': 8,
                                    'location_dest_id': 15,
                            }))
                else:
                    for bom in line_bom[0]:
                        for component in bom.bom_line_ids:
                            product1_weight1 = self.env['job.order.bom.component'].search([('product_id','=',component.product_id.id),('job_order_id','=', line.job_order_id.id)])
                            line__bom_vals.append((0,0, {
                                    'product_id': component.product_id.id,
                                    'name': component.product_id.name,
                                    'product_uom': component.product_id.uom_id.id,
                                    'product_uom_qty': product1_weight1.production_quantity,
                                    'stock_total_weight': product1_weight1.weight, 
                                    'date': fields.Date.today(),
                                    'date_expected': fields.Date.today(),
                                    'location_id': 8,
                                    'location_dest_id': 15,                                  
                            }))
                    
                            
                production_vals ={
                        'product_id': line.product_id.id,
                        'product_uom_id': line.product_id.uom_id.id,
                        'product_qty': line.production_quantity,
                        'production_total_weight':line.weight, 
                        'origin': self.job_order_id.name, 
                        'job_order_id': self.job_order_id.id, 
                        'bom_id': variant_line_bom[0].id,
                        'date_planned_start': fields.Date.today(),
                        'picking_type_id': line.picking_type_id.id,
                        'location_src_id': line.location_src_id.id,
                        'location_dest_id': line.location_dest_id.id,
                        'move_raw_ids': line__bom_vals ,
                }
                production_order = self.env['mrp.production'].create(production_vals)
                if line.production_created == False and line.type == 'normal':
                    line.update ({
                        'production_created': True,
                        })
                    
            count = count + 1        
                
          
    
    
    
    def action_generate_po(self):
        vendor_list = []
        for line in self:
            if line.vendor_id and line.po_created == False:
                vendor_list.append(line.vendor_id)
            else:
                pass
        list = set(vendor_list)
        for vendor in list:
            product_list = []
            product_uniq_list = []
            for seller_line in self:
                product_quantity = 0.0
                weight_total = 0.0
                product_count = 0
                product_uom = 0
                product_id = 0
                price = 0
                seller_product = seller_line.product_id.id
                if vendor == seller_line.vendor_id:
                    if seller_line.po_created == False:                       
                        for product_line in self:
                            if product_line.po_created == False:
                                if product_line.product_id.id == seller_product:
                                    product_quantity = product_quantity + product_line.production_quantity
                                    weight_total = weight_total + product_line.weight
                                    product_count = product_count + 1

                        if  product_count >= 2:           
                            seller_line.update({
                                'is_duplicate': True
                            })
                        if seller_line.is_duplicate == True:   
                            product_uniq_list.append(seller_line.product_id.id)
            
                                    
                        if seller_line.is_duplicate == False:
                            line_vals = {
                                'product_id': seller_line.product_id.id,
                                'name': seller_line.product_id.name,
                                'product_uom_qty': product_quantity,
                                'price_unit': seller_line.product_id.standard_price,
                                'total_weight': weight_total, 
                                'date_planned': fields.Date.today(),
                                'product_uom': seller_line.product_id.uom_po_id.id,
                            }
                            product_list.append(line_vals)

            uniq_product = set(product_uniq_list)
            for uniq_product in uniq_product:
                produt_uniq = self.env['product.product'].search([('id','=',uniq_product)])
                line_vals = {
                             'product_id': produt_uniq.id,
                             'name': produt_uniq.name,
                             'product_uom_qty': product_quantity,
                             'price_unit': produt_uniq.standard_price,
                             'total_weight': weight_total, 
                             'date_planned': fields.Date.today(),
                             'product_uom': produt_uniq.uom_po_id.id,
                                }
                product_list.append(line_vals)  
            vals = {
                  'partner_id': vendor.id,
                  'date_order': fields.Date.today(),
                  'origin' : self.job_order_id.name,
                  'job_order_id': self.job_order_id.id,
                  'sale_id': self.job_order_id.sale_id.id 
                    }
            order = self.env['purchase.order'].create(vals)
            
            for prod in product_list:
                order_line = {
                       'order_id': order.id,
                       'product_id': prod['product_id'],
                       'name': prod['name'],
                       'product_qty': prod['product_uom_qty'],
                       'price_unit': prod['price_unit'],
                       'total_weight': prod['total_weight'],
                       'date_planned': fields.Date.today(),
                       'product_uom': prod['product_uom'],
                        }
                purchase_orders_line = self.env['purchase.order.line'].create(order_line)
        for line in self:
            if line.po_created == False and line.type != 'normal' and line.vendor_id:
                line.update ({
                    'po_created': True,
                  	})
                
                
     