# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    parent_product_tmpl_id = fields.Many2one('product.template', 'Parent Product', stored=True, required=False)
    ref_product_tmpl_id = fields.Many2one('product.template', 'Reference Product', stored=True, required=False)
    ref_product_tmpl_ids = fields.One2many('product.template', 'ref_product_tmpl_id', string='Reference Products', auto_join=True)
    
    data_maintenance_lines = fields.One2many('product.data.maintain', 'product_tmpl_id', string='Maintenance Lines',  copy=True, auto_join=True)
    is_dm = fields.Boolean("Is Bom", default=False, copy=False)
    
    def action_create_master_data(self):
        consumption_qty = 0
        self.bom_ids.unlink()
        for p in self.ref_product_tmpl_ids:
            p.bom_ids.unlink()
            p.seller_ids.unlink()
        self.ref_product_tmpl_ids.unlink()
        
        parent_product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id)],limit=1)
        #create parent reorderin rule
        for route in self.categ_id.route_ids:
            if route.name in ['Buy']:
                buy_parent__id = self.env['stock.warehouse.orderpoint'].create({
                    'product_id':parent_product_id.id,
                    'product_min_qty':0,
                    'product_max_qty':0,
                    'qty_multiple':1,
                    'location_id':8,
                })
            elif route.name in ['Resupply Subcontractor on Order']:
                buy_parent__id = self.env['stock.warehouse.orderpoint'].create({
                    'product_id':parent_product_id.id,
                    'product_min_qty':0,
                    'product_max_qty':0,
                    'qty_multiple':1,
                    'location_id':19,   
                })
        for vn in self.product_variant_ids:
            parent_product_tmpl_id = self.id
            for dm in self.data_maintenance_lines:
                if not(dm.is_multi_bom):
                    parent_product_tmpl_id = self.id
                if dm.production_tolerance > 0:
                    consumption_qty = 1 + (1*(dm.production_tolerance/100))
                #create products
                product_tmpl_id = self.env['product.template'].create({
                    'name': vn.display_name + '-' + dm.categ_id.name,
                    'type':self.type,
                    'categ_id':dm.categ_id.id,
                    'sale_ok':False,
                    'purchase_ok':True,
                    'uom_id':self.uom_id.id,
                    'uom_po_id':self.uom_po_id.id,
                    'parent_product_tmpl_id': parent_product_tmpl_id,
                    'ref_product_tmpl_id': self.id,
                    'tracking': dm.tracking,
                    'weight': vn.weight or self.dim_weight,
                })
                
                product_id = self.env['product.product'].search([('product_tmpl_id', '=', product_tmpl_id.id)],limit=1)
                
                #create parent bom
                if parent_product_tmpl_id == self.id and dm.is_bom_maintenance and dm.is_multi_bom:
                    parent_bom_id = self.env['mrp.bom'].create({
                        'product_tmpl_id':self.id,
                        'product_id': vn.id,
                        'product_uom_id':self.uom_id.id,
                        'product_qty':1,
                        'type':'normal',
                    })
                    parent_bom_line = self.env['mrp.bom.line'].create({
                        'bom_id': parent_bom_id.id,
                        'product_id':product_id.id,
                        'product_qty':consumption_qty,
                    })
                parent_product_tmpl_id = product_tmpl_id.id
        
        for product in self.ref_product_tmpl_ids:
            component_product_id = self.env['product.template'].search([('parent_product_tmpl_id', '=', product.id)],limit=1)
            variant_id = self.env['product.product'].search([('product_tmpl_id', '=', product.id)],limit=1)
            component_id = self.env['product.product'].search([('product_tmpl_id', '=', component_product_id.id)],limit=1)
            dm_id = self.env['product.data.maintain'].search([('product_tmpl_id', '=', self.id),('categ_id', '=', product.categ_id.id)],limit=1)
           
            contractor_ids = self.env['res.partner'].search([('category_id', '=', dm_id.partner_tag.id)])
            contractors = []
            for rs in contractor_ids:
                contractors.append(rs.id)
                # Vendor Pricelist
                if dm_id.bom_type == 'subcontract':
                    vendor_pricelist_id = self.env['product.supplierinfo'].create({
                        'name':rs.id,
                        'min_qty':1,
                        'price':1,
                        'product_tmpl_id':product.id,
                        'is_subcontractor':True,
                    })
                
            #create bom
            if component_id and dm_id.is_bom_maintenance and dm_id.is_multi_bom:
                bom_id = self.env['mrp.bom'].create({
                    'product_tmpl_id':product.id,
                    'product_uom_id':product.uom_id.id,
                    'product_qty':1,
                    'type':dm_id.bom_type,
                    'subcontractor_ids':[( 6, 0, contractors)],
                })
                bom_line = self.env['mrp.bom.line'].create({
                    'bom_id': bom_id.id,
                    'product_id':component_id.id,
                    'product_qty':1,
                })
            elif dm_id.is_bom_maintenance and not(dm_id.is_multi_bom):
                bom_id = self.env['mrp.bom'].create({
                    'product_tmpl_id':product.id,
                    'product_uom_id':product.uom_id.id,
                    'product_qty':1,
                    'type':dm_id.bom_type,
                    'subcontractor_ids':[( 6, 0, contractors)],
                })
                bom_line = self.env['mrp.bom.line'].create({
                    'bom_id': bom_id.id,
                    'product_id':parent_product_id.id,
                    'product_qty':1,
                })
            
            #create reordering rules
            for route in product.categ_id.route_ids:
                if route.name in ['Buy','Manufacture']:
                    #child reordering rule
                    buy_op_id = self.env['stock.warehouse.orderpoint'].create({
                        'product_id':variant_id.id,
                        'product_min_qty':0,
                        'product_max_qty':0,
                        'qty_multiple':1,
                        'location_id':8,
                        
                    })
                elif route.name in ['Resupply Subcontractor on Order']:
                    sc_op_id = self.env['stock.warehouse.orderpoint'].create({
                        'product_id':variant_id.id,
                        'product_min_qty':0,
                        'product_max_qty':0,
                        'qty_multiple':1,
                        'location_id':19,
                        
                    })
        self.is_dm = True
            

class ProductDataMaintenance(models.Model):
    _name = 'product.data.maintain'
    _description = 'Product Data Maintenance'
    
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, ondelete='cascade')
    routing_id = fields.Many2one('mrp.routing', string='Routing',on_delete='setnull', required=True)
    categ_id = fields.Many2one('product.category', 'Product Category', required=True, help="Select category for the current product")
    tracking = fields.Selection([
        ('none', 'No Tracking'),
        ('lot', 'By Lot'),
        ('serial', 'By Serial')], 'Tracking',
        default='none', required=True)
    
    is_reorder_rule_maintenance = fields.Boolean("Is Reorder Rule", default=True)
    is_bom_maintenance = fields.Boolean("Is Bom", default=False)
    is_multi_bom = fields.Boolean("Is Multi-level Bom", default=True)
    bom_type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('subcontract', 'Subcontracting')], 'BoM Type',
        default='normal', required=True)
    partner_tag = fields.Many2one('res.partner.category', string='Subcontractor Category')
    production_tolerance = fields.Float(string='Tolerance', default=0.0)
    