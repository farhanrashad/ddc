# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class OrderProductionReport(models.Model):
    _name = "order.production.report"
    _description = "Order Production Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'
    
    name = fields.Char('Reference', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    global_ref = fields.Char('Global Ref.', readonly=True)
    sale_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product', readonly=True)
    product_id = fields.Many2one('product.product', 'Variant', readonly=True)
    
    order_qty = fields.Float('Order qty', readonly=True)
    order_weight = fields.Float('Order Weight', readonly=True)
    delivered_qty = fields.Float('Delivered qty', readonly=True)
    
    prd_order_qty = fields.Float('Production qty', readonly=True)
    prd_weight = fields.Float('Production Weight', readonly=True)
    
    produced_qty = fields.Float('Produced qty', readonly=True)
    produced_weight = fields.Float('produced Weight', readonly=True)
    
    remaining_qty = fields.Float('Remaining qty', readonly=True)
    remaining_weight = fields.Float('remaining Weight', readonly=True)
        
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
        count(a.*) as nbr, min(a.line_id) as id, min(a.name) as name, max(a.date_order) as date, a.id as sale_id, a.partner_id, a.global_ref, a.product_id,a.product_tmpl_id, 
sum(a.order_qty) as order_qty, sum(a.order_weight) as order_weight, sum(a.qty_delivered) as delivered_qty,
sum(a.prd_order_qty) as prd_order_qty, sum(a.production_weight) as prd_weight, sum(a.produced_qty) as produced_qty, 0 as produced_weight, sum(a.prd_order_qty)-sum(a.produced_qty) as remaining_qty, 0 as remaining_weight from (
select so.id, m.id as line_id, so.partner_id, so.global_ref, m.name,so.date_order, m.product_id, p.product_tmpl_id, 
0 as order_qty, 0 as order_weight, 0 as qty_delivered,
m.product_qty as prd_order_qty, m.production_weight, (select sum(move.product_qty) from stock_move move join stock_location loc on move.location_dest_id = loc.id where move.state = 'done' and loc.usage='internal' and move.product_id = m.product_id and move.production_id = m.id ) as produced_qty
from mrp_production m
join sale_order so on m.ref_sale_id = so.id
join product_product p on m.product_id = p.id
join product_template pt on p.product_tmpl_id = pt.id
) a
group by a.partner_id, a.global_ref, a.id,a.product_tmpl_id, a.product_id
        
        """

        for field in fields.values():
            select_ += field
        
        from_ = groupby_ = ''

        return '%s (SELECT %s %s %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))