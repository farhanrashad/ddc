# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#################################################################################

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError

class ExtraIssuanceReport(models.AbstractModel):
    _name = 'report.de_extra_issuance.stock_extra_issuance'
    _description = 'Extra Issuance Report'

    '''Find Purchase invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        outstanding_invoice = [] 
        product_list = []
        bom_product = []
        all_boms = []
        for sale in docs.articles_lines: 
            article_qty = sale.quantity
            product_variant_bom = self.env['mrp.bom'].search([('product_id','=',sale.product_id.id)])
            product_tmpl_bom = self.env['mrp.bom'].search([('product_tmpl_id.name','=',sale.product_id.name)])
            if product_variant_bom:
                if product_variant_bom.type == 'normal' and product_variant_bom.product_id.categ_id.id !=81:
                    if product_variant_bom.product_id.categ_id.id !=85:
                        bom_vals = {
                               'id': product_variant_bom.product_id.id,
                               'product_id': product_variant_bom.product_id.name,
                               'product_uom_id': product_variant_bom.product_id.uom_id.id,
                               'component_qty': product_variant_bom.product_qty * article_qty,
                                 }
                        bom_product.append(bom_vals)
                
                for component_level1 in product_variant_bom.bom_line_ids:
                    if  component_level1.product_id.categ_id.id != 81:
                        if  component_level1.product_id.categ_id.id != 85:
                            bom_vals = {
                           'id': component_level3.product_id.id,
                           'product_id': component_level1.product_id.name,
                           'product_uom_id': component_level1.product_id.uom_id.name,
                           'component_qty': component_level1.product_qty * article_qty,
                             }
                            bom_product.append(bom_vals)        
                    component_bom_level2 = self.env['mrp.bom'].search([('product_id','=',component_level1.product_id.id),('type','=','normal')])
                    for component_level2 in component_bom_level2.bom_line_ids:
                        if component_level2.product_id.categ_id.id != 81:
                            if  component_level2.product_id.categ_id.id != 85:
                                bom_vals = {
                               'id': component_level2.product_id.id,
                               'product_id': component_level2.product_id.name,
                               'product_uom_id': component_level2.product_id.uom_id.name,
                               'component_qty': component_level2.product_qty * article_qty,
                                 }
                                bom_product.append(bom_vals)   
                        component_bom_level3 = self.env['mrp.bom'].search([('product_id','=',component_level2.product_id.id),('type','=','normal')])        
                         
                        for component_level3 in component_bom_level3.bom_line_ids:
                            if component_level3.product_id.categ_id.id != 81:
                                if component_level3.product_id.categ_id.id != 85:
                                    bom_vals = {
                                    'id': component_level3.product_id.id,
                                   'product_id': component_level3.product_id.name,
                                   'product_uom_id': component_level3.product_id.uom_id.name,
                                   'component_qty': component_level3.product_qty * article_qty,
                                     }
                                    bom_product.append(bom_vals) 
                                
                            component_bom_level4 = self.env['mrp.bom'].search([('product_id','=',component_level3.product_id.id),('type','=','normal')])     
                              
                            for component_level4 in component_bom_level4.bom_line_ids:
                                if component_level4.product_id.categ_id.id != 81:
                                    if component_level4.product_id.categ_id.id != 85:
                                        bom_vals = {
                                       'id': component_level4.product_id.id,
                                       'product_id': component_level4.product_id.name,
                                       'product_uom_id': component_level4.product_id.uom_id.name,
                                       'component_qty': component_level4.product_qty * article_qty,
                                         }
                                        bom_product.append(bom_vals)   
                                    
                                component_bom_level5 = self.env['mrp.bom'].search([('product_id','=',component_level4.product_id.id),('type','=','normal')])  
                                
                                for component_level5 in component_bom_level5.bom_line_ids:
                                    if component_level5.product_id.categ_id.id != 81:
                                        if component_level5.product_id.categ_id.id != 85:

                                            bom_vals = {
                                           'id': component_level5.product_id.id,
                                           'product_id': component_level5.product_id.name,
                                           'product_uom_id': component_level5.product_id.uom_id.name,
                                           'component_qty': component_level5.product_qty * article_qty,
                                             }
                                            bom_product.append(bom_vals)                                               
                                    component_bom_level6 = self.env['mrp.bom'].search([('product_id','=',component_level5.product_id.id)])  
                                    
                                    for component_level6 in component_bom_level6.bom_line_ids:
                                        if component_level6.product_id.categ_id.id != 81: 
                                            if component_level6.product_id.categ_id.id != 85: 
                                               
                                                bom_vals = {
                                                'id': component_level6.product_id.id,
                                                'product_id': component_level6.product_id.name,
                                                'product_uom_id': component_level6.product_id.uom_id.name,
                                                'component_qty': component_level6.product_qty * article_qty,
                                                  }
                                                bom_product.append(bom_vals)  
                                                
                                                
        duplicate_product = []
        uniq_list = []
        for product in bom_product:
            duplicate_product.append(product['id'])
        uniq_product = set(duplicate_product)
        for uniq in uniq_product:
            product_name = ' '
            component_qty  = 0.0
            uom_id = ' '
            for product in bom_product:
                if uniq == product['id']:
                    component_qty = component_qty + product['component_qty']
                    product_name =  product['product_id']
                    uom_id = product['product_uom_id']
            uniq_list.append({
                'product_id': product_name,
                'uom_id': uom_id,
                'component_qty': component_qty,
                })    
            
    
                                                        
        if uniq_list:        
            return {
                'docs': docs,
                'bom_product': uniq_list,               
            }
        else:
            raise UserError("There is not any Purchase invoice in between selected dates")

            
    
