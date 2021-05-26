# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    def compute_section_sums(self):
        bal = 0
        qty = 0
        weight = 0
        count = 0
        for line in self.order_line:
            bal += line.price_subtotal
            qty += line.product_uom_qty
            weight += line.total_weight
            count = count + 1
            if line.display_type == 'line_section':
                name = str(line.name).split(' Q')[0] 
                if count == 1:
                    line.write({
                        'name': name })
                else:
                    quantity = '        Quantity: ' + str(qty)
                    weight = '        Total Weight: ' + str(weight)
                    subtotal = '        SubTotal: ' + str(bal)
                    line.write({
                        'name': name + quantity + weight + subtotal })
                count = count + 1
                bal = 0
                qty = 0
                weight = 0
            self.section_sum = 0
            
    section_sum = fields.Float('Section Sum', compute='compute_section_sums')
    
    
class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    def compute_section_sums(self):
        bal = 0
        qty = 0
        weight = 0
        count = 0
        for line in self.order_line:
            bal += line.price_subtotal
            qty += line.product_qty
            weight += line.total_weight
            count = count + 1
            if line.display_type == 'line_section':
                if count == 1:
                    line.write({
                        'name': str(line.name).split(' Q')[0] 
                        })
                else:
                    quantity = '        Quantity: ' + str(qty)
                    weight = '        Total Weight: ' + str(weight)
                    subtotal = '        SubTotal: ' + str(bal)
                    line.write({
                        'name': str(line.name).split(' Q')[0] + quantity + weight + subtotal
                        })
                count = count + 1
                bal = 0
                qty = 0
                weight = 0
            self.section_sum = 0
            
    section_sum = fields.Float('Section Sum', compute='compute_section_sums')