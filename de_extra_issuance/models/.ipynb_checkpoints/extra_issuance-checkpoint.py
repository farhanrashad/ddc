# -*- coding: utf-8 -*-



from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_round



class ExtraIssuance(models.Model):

    _inherit = 'mrp.bom'

    def _recursive_boms(self):
        """
        @return: returns a list of tuple (id) which are all the children of the passed bom_ids
        """
        children_boms = []
        for bom in self.filtered(lambda bom: bom.bom_line_ids.product_id.product_tmpl_id.bom_ids):
            children_boms += bom.bom_line_ids.product_id.product_tmpl_id.bom_ids._recursive_boms()
        return [(bom.id) for bom in self] + children_boms
    

class ExtraIssuance(models.Model):

    _name = 'extra.issuance'
    _rec_name = 'sale_id'
    
    def action_view_picking(self):
        self.ensure_one()
        return {
         'type': 'ir.actions.act_window',
         'binding_type': 'object',
         'domain': [('origin', '=', self.name)],
         'multi': False,
         'name': 'Picking',
         'target': 'current',
         'res_model': 'stock.picking',
         'view_mode': 'tree,form',
        }
    
    
    @api.onchange('sale_id')
    def _onchange_invoice_date(self):
        data = []
        for line in self.sale_id.order_line:
            if line.display_type != 'line_section':
                data.append(line.product_id.id)
        self.product_line_ids = data

    def get_picking_count(self):
        count = self.env['stock.picking'].search_count([('origin', '=', self.name)])
        self.picking_count = count
        
    picking_count = fields.Integer(string='Picking', compute='get_picking_count')    
    product_line_ids = fields.Many2many('product.product', string="Product",)
    
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('extra.issuance') or _('New')    
        res = super(ExtraIssuance,self).create(vals)
        return res
    
    def unlink(self):
        for isuance in self:
            if isuance.state in ('processed','submitted','approved'):
                raise UserError(_('You cannot delete an Document  which is not draft or cancelled.'))
     
            return super(ExtraIssuance, self).unlink()

    
    name = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))    
    sale_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    reason = fields.Char(string='Reason', required=True)
    articles_lines = fields.One2many('extra.issuance.article.line', 'article_id')
    component_lines = fields.One2many('extra.issuance.component.line', 'component_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processed', 'Processed'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved')],
        readonly=True, index=True, copy=False, default='draft')
    
    
            
            
            
        

    def action_process(self):
        uniq_products = []
        product_list = []
        bom_product = []
        all_boms = []
        for sale in self.articles_lines: 
            article_qty = sale.quantity
            product_variant_bom = self.env['mrp.bom'].search([('product_id','=',sale.product_id.id)])
            product_tmpl_bom = self.env['mrp.bom'].search([('product_tmpl_id.name','=',sale.product_id.name)])
            if product_variant_bom:
                if product_variant_bom.type == 'normal' and product_variant_bom.product_id.categ_id.id !=81:
                    if product_variant_bom.product_id.categ_id.id !=85:
                        for existing_component in self.component_lines:
                            if existing_component.product_id.id ==  product_variant_bom.product_id.id: 
                                quant= existing_component.component_qty
                            else:
                                uniq_products.append(product_variant_bom.product_id.id)
                                bom_vals = {
                               'component_id': self.id,
                               'product_id': product_variant_bom.product_id.id,
                               'component_qty': product_variant_bom.product_qty * article_qty,
                                 }
                                bom_product.append(bom_vals)
                
                for component_level1 in product_variant_bom.bom_line_ids:
                    if  component_level1.product_id.categ_id.id != 81:
                        if  component_level1.product_id.categ_id.id != 85:
                            uniq_products.append(component_level1.product_id.id)
                            bom_vals = {
                           'component_id': self.id,
                           'product_id': component_level1.product_id.id,
                           'component_qty': component_level1.product_qty * article_qty,
                             }
                            bom_product.append(bom_vals)        
                    component_bom_level2 = self.env['mrp.bom'].search([('product_id','=',component_level1.product_id.id),('type','=','normal')])
                    for component_level2 in component_bom_level2.bom_line_ids:
                        if component_level2.product_id.categ_id.id != 81:
                            if  component_level2.product_id.categ_id.id != 85:
                                uniq_products.append(component_level2.product_id.id)
                                bom_vals = {
                               'component_id': self.id,
                               'product_id': component_level2.product_id.id,
                               'component_qty': component_level2.product_qty * article_qty,
                                 }
                                bom_product.append(bom_vals)   
                        component_bom_level3 = self.env['mrp.bom'].search([('product_id','=',component_level2.product_id.id),('type','=','normal')])        
                         
                        for component_level3 in component_bom_level3.bom_line_ids:
                            if component_level3.product_id.categ_id.id != 81:
                                if component_level3.product_id.categ_id.id != 85:
                                                                    
                                    uniq_products.append(component_level3.product_id.id)
                                    bom_vals = {
                                   'component_id': self.id,
                                   'product_id': component_level3.product_id.id,
                                   'component_qty': component_level3.product_qty * article_qty,
                                     }
                                    bom_product.append(bom_vals) 
                                
                            component_bom_level4 = self.env['mrp.bom'].search([('product_id','=',component_level3.product_id.id),('type','=','normal')])     
                              
                            for component_level4 in component_bom_level4.bom_line_ids:
                                if component_level4.product_id.categ_id.id != 81:
                                    if component_level4.product_id.categ_id.id != 85:
                                        uniq_products.append(component_level4.product_id.id)

                                        bom_vals = {
                                       'component_id': self.id,
                                       'product_id': component_level4.product_id.id,
                                       'component_qty': component_level4.product_qty * article_qty,
                                         }
                                        bom_product.append(bom_vals)   
                                    
                                component_bom_level5 = self.env['mrp.bom'].search([('product_id','=',component_level4.product_id.id),('type','=','normal')])  
                                
                                for component_level5 in component_bom_level5.bom_line_ids:
                                    if component_level5.product_id.categ_id.id != 81:
                                        if component_level5.product_id.categ_id.id != 85:
                                            uniq_products.append(component_level5.product_id.id)
 
                                            bom_vals = {
                                           'component_id': self.id,
                                           'product_id': component_level5.product_id.id,
                                           'component_qty': component_level5.product_qty * article_qty,
                                             }
                                            bom_product.append(bom_vals)                                               
                                    component_bom_level6 = self.env['mrp.bom'].search([('product_id','=',component_level5.product_id.id)])  
                                    
                                    for component_level6 in component_bom_level6.bom_line_ids:
                                        if component_level6.product_id.categ_id.id != 81: 
                                            if component_level6.product_id.categ_id.id != 85: 
                                                uniq_products.append(component_level6.product_id.id)

                                                bom_vals = {
                                                'component_id': self.id,
                                                'product_id': component_level6.product_id.id,
                                                'component_qty': component_level6.product_qty * article_qty,
                                                  }
                                                bom_product.append(bom_vals)    
                                                
        duplicate_product = []
        uniq_list = []
        data2 = []
        self.product_line_ids = uniq_list
        for product in bom_product:
            duplicate_product.append(product['product_id'])
        uniq_product = set(uniq_products)
        for prodcut in uniq_product:
            data2.append(prodcut)
        for uniq in uniq_product:
            product_name = ' '
            component_qty  = 0.0
            for product in bom_product:
                if uniq == product['product_id']:
                    component_qty = component_qty + product['component_qty']
                    product_name =  product['product_id']
            uniq_list.append({
                'product_id': product_name,
                'component_id': self.id,
                'component_qty': component_qty,
                }) 
            
        self.product_line_ids = uniq_products    
        for line in self.articles_lines:
            line.update({
                'is_processed': True
            })
            

            
        
        self.write({'state': 'processed'})
    
    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        picking_delivery = self.env['stock.picking.type'].search([('id', '=', 6)], limit=1)
        vals = {
            'location_id': picking_delivery.default_location_src_id.id,
            'location_dest_id': picking_delivery.default_location_dest_id.id,
            'picking_type_id': picking_delivery.id,
            'origin': self.name,
            'sale_ref': self.sale_id.name,
        }
        picking = self.env['stock.picking'].create(vals)
        print('header created')
        for line in self.component_lines:
            lines = {
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'name': 'Internal Transfer',
                'product_uom': line.product_id.product_tmpl_id.uom_id.id,
                'location_id': picking_delivery.default_location_src_id.id,
                'location_dest_id': picking_delivery.default_location_dest_id.id,
                'product_uom_qty': line.component_qty,
            }
            stock_move = self.env['stock.move'].create(lines)

        self.write({'state': 'approved'})       

    product_ids = fields.One2many('extra.issuance.article.line','product_id',string="Lines")

class ExtraIssuanceArticleLine(models.Model):
    _name = 'extra.issuance.article.line'
    
    
    article_id = fields.Many2one('extra.issuance', string="Article")
    is_processed = fields.Boolean(string="Is Processed")
    product_line_ids = fields.Many2many(related="article_id.product_line_ids", string="Product",)
    product_id = fields.Many2one('product.product', string='Product', domain="[('id', 'in', product_line_ids)]")
    quantity = fields.Float(string='Quantity')
    
    
class ExtraIssuanceComponentLine(models.Model):
    _name = 'extra.issuance.component.line'

    component_id = fields.Many2one('extra.issuance')
    product_line_ids = fields.Many2many(related="component_id.product_line_ids", string="Product",)
    product_id = fields.Many2one('product.product', string='Component', domain="[('id', 'in', product_line_ids)]")
    component_qty = fields.Float(string='Total Quantity',  digits='Product Unit of Measure',)
    
    
