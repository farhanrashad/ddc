# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class MRPProduction(models.Model):
    _inherit = 'mrp.production'
    
    def button_mark_done(self):
        res = super(MRPProduction,self).button_mark_done()
        sale = self.env['sale.order'].search([('id','=',self.ref_sale_id.id)])
        sale.update({
            'production_status':self.product_id.categ_id.name + ' Produced'
        })
        return res
    
    def action_confirm(self):
        res = super(MRPProduction,self).action_confirm()
        sale = self.env['sale.order'].search([('id','=',self.ref_sale_id.id)])
        sale.update({
            'production_status':self.product_id.categ_id.name + ' In-Production'
        })
        return res