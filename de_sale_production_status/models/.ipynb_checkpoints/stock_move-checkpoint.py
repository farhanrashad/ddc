# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    def _action_done1(self):
        res = super(StockMove,self)._action_done()
        sale = self.env['sale.order'].search([('id','=',self.sale_id.id)])
        picking = self.env['stock.picking'].search([('id','=',self.move_id.picking_id.id)],limit=1)
        
        sale.update({
            'production_status': (self.product_id.categ_id.name + ' ' + str(self.picking_id.picking_type_id.name))
        })
        return res
    
    def write(self, vals):
        res = super(StockMove,self).write(vals)
        sale = self.env['sale.order'].search([('id','=',self.ref_sale_id.id)])
        for line in self:
            sale.update({
                'production_status': line.product_id.categ_id.name + ' ' + str(line.picking_type_id.name)
            })
        return res