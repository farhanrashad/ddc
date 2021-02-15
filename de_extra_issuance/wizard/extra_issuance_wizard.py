# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Dynexcel Business Solution <www.dynexcel.com>

#
#################################################################################

from odoo import api, fields, models, _

class ExtraIssuance(models.TransientModel):
    _name = "extra.issuance.wizard"
    _description = "Extra Issuance wizard"
    
    @api.onchange('sale_id')
    def _onchange_invoice_date(self):
        data = []
        if self.sale_id:
            for line in self.sale_id.order_line:
                if line.display_type != 'line_section':
                    data.append(line.product_id.id)
            self.product_line_ids = data
        if self.sale_id:
            self.is_order= True
        else:
            self.is_order= False
            

    product_line_ids = fields.Many2many('product.product', string="Product",)
    is_order = fields.Boolean(string="Is Order")
    sale_id = fields.Many2one('sale.order',string='Sale Order', help='select start date')
    articles_lines = fields.One2many('extra.issuance.wizard.line', 'article_id')
    articles_lines2 = fields.One2many('extra.issuance.wizard.line2', 'article_id')
    

    def check_report(self):
        data = {}
        data['form'] = self.read(['sale_id', 'articles_lines'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['sale_id', 'articles_lines'])[0])
        return self.env.ref('de_extra_issuance.open_extra_issuance_action').with_context(landscape=True).report_action(
            self, data=data, config=False)
    
    
class ExtraIssuanceLine(models.TransientModel):
    _name = "extra.issuance.wizard.line"
    _description = "Extra Issuance wizard line" 
    
    
    @api.onchange('product_id')
    def _compute_product_quantity(self):
        for line in self:
            for product in line.article_id.sale_id.order_line:
                if line.product_id.id == product.product_id.id:
                    
                    line.update({
                        'product_quantity': product.product_uom_qty,
                    })


    
    article_id = fields.Many2one('extra.issuance.wizard', string="Extra Issuance")
    product_line_ids = fields.Many2many(related="article_id.product_line_ids", string="Product",)
    product_quantity = fields.Float(string="Product Quantity", )
    product_id = fields.Many2one('product.product', string='Product', domain="[('id', 'in', product_line_ids)]")
    quantity = fields.Float(string='Quantity')


    
    
class ExtraIssuanceLine2(models.TransientModel):
    _name = "extra.issuance.wizard.line2"
    _description = "Extra Issuance wizard line" 
    
    
    @api.onchange('product_id')
    def _compute_product_quantity(self):
        for line in self:
            for product in line.article_id.sale_id.order_line:
                if line.product_id.id == product.product_id.id:
                    
                    line.update({
                        'product_quantity': product.product_uom_qty,
                    })


    
    article_id = fields.Many2one('extra.issuance.wizard', string="Extra Issuance")
    product_line_ids = fields.Many2many(related="article_id.product_line_ids", string="Product",)
    product_quantity = fields.Float(string="Product Quantity", )
    product_id = fields.Many2one('product.product', string='Product',)
    quantity = fields.Float(string='Quantity')
    
