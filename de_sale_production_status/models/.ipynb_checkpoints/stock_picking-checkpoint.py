# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    def button_validate(self):
        category = ''
        sale = self.env['sale.order'].search([('id','=',self.ref_sale_id.id)])
        for line in self.move_ids_without_package:
            if line.quantity_done:
                category = line.product_id.categ_id.name
        
        sale.update({
            'production_status': (category + ' ' + self.picking_type_id.name)
        })
        res = super(StockPicking,self).button_validate()
        return res