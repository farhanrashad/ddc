# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleStockReport(models.Model):
    _name = "sale.stock.report"
    _description = "Sale Stock Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'
    
    name = fields.Char('Reference', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    
    sale_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    location_id = fields.Many2one('stock.location', 'Location', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product', readonly=True)
    product_id = fields.Many2one('product.product', 'Variant', readonly=True)
    
    quantity = fields.Float('Quantity', readonly=True)
    product_weight = fields.Float('Weight', readonly=True)
    
        
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
        count(a.*) as nbr, min(a.sale_id) as id, min(a.sale_id) as name, max(a.date) as date, a.sale_id, a.location_id, a.categ_id, a.product_tmpl_id, a.product_id, sum(a.quantity) as quantity, sum(a.product_weight) as product_weight from (
select m.product_id, m.sale_id, m.date, q.quantity, q.product_weight, q.location_id, t.categ_id, p.product_tmpl_id
from stock_move m
join stock_quant q on q.product_id = m.product_id
join stock_location l on q.location_id = l.id
join product_product p on m.product_id = p.id
join product_template t on p.product_tmpl_id = t.id
where m.sale_id IS NOT NULL
and l.usage = 'internal'
) a
group by a.sale_id, a.location_id, a.product_tmpl_id, a.product_id, a.categ_id
        
        """

        for field in fields.values():
            select_ += field
        
        from_ = groupby_ = ''

        return '%s (SELECT %s %s %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))