# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    def button_confirm(self):
        res = super(PurchaseOrder,self).button_confirm()
        sale = self.env['sale.order'].search([('id','=',self.sale_id.id)])
        category = ''
        for line in self.order_line:
            category = line.product_id.categ_id.name
        sale.update({
            'production_status': category + ' In-Process'
        })
        return res
    
    def button_done(self):
        res = super(PurchaseOrder,self).button_done()
        sale = self.env['sale.order'].search([('id','=',self.sale_id.id)])
        category = ''
        for line in self.order_line:
            category = line.product_id.categ_id.name
        sale.update({
            'production_status': category + ' Processed'
        })
        return res
    
    