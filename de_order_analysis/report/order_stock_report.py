# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class OrderStockReport(models.Model):
    _name = "order.stock.report"
    _description = "Order Stock Report"
    _auto = False
    _rec_name = 'name'
    _order = 'name'
    
    name = fields.Char('Reference', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product', readonly=True)
    product_id = fields.Many2one('product.product', 'Product Variant', readonly=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)
    
    product_uom_qty = fields.Float('Qty Ordered', readonly=True)
    order_weight = fields.Float('Order Weight', readonly=True)

    qty_delivered = fields.Float('Qty Delivered', readonly=True)
    qty_receipt = fields.Float('Qty Receipt', readonly=True)
    diff_qty = fields.Float('Qty Diff.', readonly=True)
    
    weight_delivered = fields.Float('Weight Delivered', readonly=True)
    weight_receipt = fields.Float('Weight Receipt', readonly=True)
    diff_weight = fields.Float('Weight Diff.', readonly=True)
    
    remaining_qty = fields.Float('Remaining Qty', readonly=True)
    remaining_weight = fields.Float('Remaining Weight', readonly=True)
    
    job_order = fields.Char('Job Order', readonly=True)
    global_ref = fields.Char('Global Ref.', readonly=True)
    
    team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    code = fields.Char('Picking Type', readonly=True)
    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
         count(x.*) as nbr, min(x.id) as id, x.global_ref, x.name as name,x.date, x.categ_id, x.product_tmpl_id, x.product_id, x.product_uom, sum(x.product_uom_qty) as product_uom_qty, sum(x.order_weight) as order_weight, x.job_order, sum(x.qty_receipt) as qty_receipt, sum(x.qty_delivered) as qty_delivered, sum(x.qty_receipt) - sum(x.qty_delivered) as diff_qty, sum(x.weight_receipt) as weight_receipt, sum(x.weight_delivered) as weight_delivered, sum(x.weight_receipt) - sum(x.weight_delivered) as diff_weight, sum(x.product_uom_qty) - sum(x.qty_receipt) as remaining_qty, sum(x.order_weight) - sum(x.weight_receipt) as remaining_weight, x.team_id, x.partner_id, x.company_id, x.code from (
select o.id, so.global_ref, so.name as name, o.date, t.categ_id, m.product_tmpl_id, l.product_id as product_id, t.uom_id as product_uom, sl.product_uom_qty, sl.total_weight as order_weight, j.name as job_order, 
(case when ld.usage='internal' and ls.usage !='internal' then l.qty_done else 0 end) as qty_receipt, 
(case when ls.usage='internal' and ld.usage !='internal' then l.qty_done else 0 end) as qty_delivered,
(case when ld.usage='internal' and ls.usage !='internal' then l.total_weight else 0 end) as weight_receipt, 
(case when ls.usage='internal' and ld.usage !='internal' then l.total_weight else 0 end) as weight_delivered,
p.team_id, o.partner_id, o.company_id, pt.code
from stock_move o
join stock_move_line l on l.move_id = o.id
join stock_location ls on o.location_id = ls.id
join stock_location ld on o.location_dest_id = ld.id
join stock_picking k on l.picking_id = k.id
join stock_picking_type pt on k.picking_type_id = pt.id
join sale_order so on l.sale_id = so.id
join sale_order_line sl on sl.order_id = so.id
join job_order j on l.ref_job_order_id = j.id
left join res_partner p on o.partner_id = p.id
join product_product m on o.product_id = m.id
join product_template t on m.product_tmpl_id = t.id
join product_category c on t.categ_id = c.id
join res_company b on o.company_id = b.id
left join crm_team r on p.team_id = r.id
where o.state = 'done'
) x
group by x.global_ref, x.name, x.date, x.categ_id, x.product_tmpl_id, x.product_id, x.product_uom,x.job_order,x.team_id,x.partner_id,x.company_id,x.code
"""

        for field in fields.values():
            select_ += field
        
        from_ = groupby_ = ''

        return '%s (SELECT %s %s %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))