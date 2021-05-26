# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class OrderSubcontractingReport(models.Model):
    _name = "order.subcontract.report"
    _description = "Subcontracting Order Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'
    
    name = fields.Char('Reference', readonly=True)
    global_ref = fields.Char('Global Ref.', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product_category', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    sale_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    
    order_qty = fields.Float('Order qty', readonly=True, )
    order_weight = fields.Float('Order Weight', readonly=True, )
    
    received_qty = fields.Float('Received qty', readonly=True)
    received_weight = fields.Float('Received Weight', readonly=True)
    
    remaining_qty = fields.Float('Remaining Qty', readonly=True)
    remaining_weight = fields.Float('Remaining Weight', readonly=True)
    
    consumed_qty = fields.Float('Cons.qty', readonly=True)
    consumed_weight = fields.Float('Cons.Weight', readonly=True)
    
    diff_qty = fields.Float('Diff.Qty', readonly=True)
    diff_weight = fields.Float('Diff.Weight', readonly=True)
    
    issued_qty = fields.Float('Issued Qty', readonly=True)
    issued_weight = fields.Float('Issued Weight', readonly=True)
    
    supplier_diff_qty = fields.Float('Sup.Diff.Qty', readonly=True)
    supplier_diff_weight = fields.Float('Sup.Diff.(Kg)', readonly=True)
    
    
    
    #@api.model
    @api.depends('product_id')
    def _calcualte_order_qty(self):
        self.ensure_one()
        sum_qty = 0
        sum_weight = 0
        #line = order_lines = self.env['purchase.order.line'].search([('product_id','=',0)])
        
        query = '''
            SELECT sum(product_qty) from purchase_order_line
            
        '''
        #params = [self.product_id.id]
        self._cr.execute(query)
        sum_qty = self._cr.fetchone()
        return sum_qty
        #for order in self:    
        #if self.product_id:
        #line = order_lines = self.env['purchase.order.line']
        #order_lines = self.env['purchase.order.line'].search([('product_id','=',self.product_id.id),('order_id.sale_id','=',self.sale_id.id)])    
        #for line in order_lines:
        #for line in self._cr.dictfetchall():
            #sum_qty += line['product_qty']
            #sum_weight += line.total_weight
        #self.order_qty = sum_qty
        #self.order_weight = sum_weight
        #self.remain_qty = sum_qty - self.produced_qty
        #self.remain_weight = sum_weight -  self.produced_weight
        
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
        count(a.*) as nbr, min(a.id) as id, min(a.name) as name, max(date_order) as date, a.sale_id, a.global_ref, a.partner_id, a.categ_id, a.product_id, sum(a.order_qty) as order_qty, sum(a.order_weight) as order_weight, sum(a.received_qty) as received_qty, sum(a.received_weight) as received_weight, sum(a.issued_qty) as issued_qty, sum(a.issued_weight) as issued_weight, sum(a.consumed_qty) as consumed_qty, sum(a.consumed_weight) as consumed_weight, sum(a.order_qty - a.received_qty) as remaining_qty, sum(a.order_weight - a.received_weight) as remaining_weight, sum(a.received_qty - a.consumed_qty) as diff_qty, sum(a.received_weight - a.consumed_weight) as diff_weight, sum(a.received_qty - a.issued_qty) as supplier_diff_qty, sum(a.received_weight - a.issued_weight) as supplier_diff_weight from (
select po.id, po.sale_id,so.global_ref,po.date_order, po.partner_id,po.name, pt.categ_id, pl.product_id,pl.product_qty as order_qty, pl.total_weight as order_weight, pl.qty_received as received_qty, 0 as received_weight, pl.qty_issued as issued_qty, pl.weight_issued as issued_weight, pl.qty_consume as consumed_qty, pl.weight_consume as consumed_weight
from purchase_order po 
join purchase_order_line pl on pl.order_id = po.id
join product_product pp on pl.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
left join sale_order so on po.sale_id = so.id
) a
group by a.sale_id, a.global_ref, a.partner_id, a.categ_id, a.product_id
        
        """

        for field in fields.values():
            select_ += field
        
        from_ = groupby_ = ''

        return '%s (SELECT %s %s %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))