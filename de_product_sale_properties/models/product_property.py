# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class ProductTemplateAttributeLines(models.Model):
    _inherit = "product.template.attribute.line"
    
    @api.onchange('attribute_id')
    def onchange_attribute(self):
        self.value_ids = self.env['product.attribute.value'].search([('attribute_id','=', self.attribute_id.id)])

    
    
class product_properties(models.Model):
    _name='product.properties'
    _description='Product Properties'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
 
    name=fields.Char('Name')
    product_property_order_line=fields.One2many('product.properties.line','product_property',string="Product Properties")
    is_short = fields.Boolean(string="Is Short") 
    is_long = fields.Boolean(string="Is Long")
    
class product_property_line(models.Model):
    _name='product.properties.line'
    
    product_property=fields.Many2one("product.properties",string="Product Property Order") 
    name = fields.Char(string="Short Value",required=True)
    description = fields.Char(string="Long Value",required=False)
    

    
class product_tmplt(models.Model):
    _inherit='product.template'
    
    product_property_line=fields.One2many('product.properties.lines','property_ids',string="Product Property Lines")
    internal_code = fields.Char('Fabric Code')
    pct_code = fields.Char(string='PCT Code')
    
    fabric_id = fields.Many2one('product.product', string="Fabric", domain="[('categ_id.name', '=ilike', 'COATS%')]") 
    
    @api.onchange('fabric_id')
    def onchange_property(self):
        product_property = self.env['product.product'].search([('name','=', self.fabric_id.name)])
        data = []
        for property in product_property:
            for item in property.product_property_line:
                data.append((0,0,{
                            'product_property_id': item.product_property_id.id,
                            'description': item.description,
                            'product_property_line_id': item.product_property_line_id.id,
                            }))
        self.product_property_line = data
        
    

class product_template_line(models.Model):
    _name='product.properties.lines'
    _order = 'sequence'

    property_ids=fields.Many2one('product.template',string="Product Property Line", required=True)
    product_property_id=fields.Many2one("product.properties",string="Product Property", required=True) 
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    product_property_line_id=fields.Many2one("product.properties.line",  string="Short Value", domain="[('product_property', '=', product_property_id)]")
    description = fields.Char(related='product_property_line_id.description', string='Long Value', store=True)
    
    is_short = fields.Boolean(related="product_property_id.is_short") 
    is_long = fields.Boolean(related="product_property_id.is_long" )