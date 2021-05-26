# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    product_weight = fields.Float('Total Weight', compute="_calculate_total_weight", )
    
    def _calculate_total_weight(self):
        for line in self:
            query = """
        select coalesce(sum(a.total_weight),0) as total_weight from (
select l.total_weight as total_weight, l.lot_id from stock_move m 
join stock_move_line l on l.move_id = m.id
join stock_location t on l.location_dest_id = t.id
where t.usage = 'internal' and m.state = 'done'
union
select l.total_weight*-1 as total_weight, l.lot_id from stock_move m
join stock_move_line l on l.move_id = m.id
join stock_location t on l.location_id = t.id
where t.usage = 'internal' and m.state='done'
) a
where a.lot_id = %(lot_id)s
"""
            
            params = {
                'lot_id': line.id or 0,
            }
            self.env.cr.execute(query, params=params)
            for order in self._cr.dictfetchall():
                line.update({
                    'product_weight': order['total_weight']
                })