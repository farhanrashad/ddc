# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class OrderAnalysis(models.Model):
    _name = "order.analysis"
    _description = "Order Analysis Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'
    
    name = fields.Char('Reference', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product', readonly=True)
    product_id = fields.Many2one('product.product', 'Product Variant', readonly=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)
    product_uom_qty = fields.Float('Qty Ordered', readonly=True)
    qty_delivered = fields.Float('Qty Delivered', readonly=True)
    order_weight = fields.Float('Order Weight', readonly=True)
    job_order = fields.Char('Job Order', readonly=True)
    global_ref = fields.Char('Global Ref.', readonly=True)
    in_qty = fields.Float('In Qty', readonly=True)
    out_qty = fields.Float('Out Qty', readonly=True)
    in_weight = fields.Float('In Weight', readonly=True)
    out_weight = fields.Float('Out Weight', readonly=True)
    
    team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
         count(x.*) as nbr, min(x.id) as id, x.global_ref, x.name as name,x.date, x.categ_id, x.product_tmpl_id, x.product_id, x.product_uom, sum(x.product_uom_qty) as product_uom_qty, sum(x.qty_delivered) as qty_delivered, sum(x.order_weight) as order_weight, x.job_order, sum(x.in_qty) as in_qty, sum(x.out_qty) as out_qty, sum(x.in_weight) as in_weight, sum(x.out_weight) as out_weight, x.team_id, x.partner_id, x.company_id, x.user_id from (
            select l.id, o.global_ref, o.name as name,o.date_order as date, t.categ_id, m.product_tmpl_id, l.product_id as product_id, t.uom_id as product_uom, l.product_uom_qty, l.qty_delivered, l.total_weight as order_weight, j.name as job_order, 0 as in_qty, 0 as out_qty, 0 as in_weight, 0 as out_weight, o.team_id, o.partner_id, o.company_id, o.user_id
from job_order j
join sale_order o on j.sale_id = o.id
join res_partner p on o.partner_id = p.id
join sale_order_line l on l.order_id = o.id
join product_product m on l.product_id = m.id
join product_template t on m.product_tmpl_id = t.id
join product_category c on t.categ_id = c.id
left join res_company b on o.company_id = b.id
left join res_users u on o.user_id = u.id
left join crm_team r on o.team_id = r.id
where o.state in ('done','sale')
union all
select l.id, o.global_ref, o.name as name,o.date_order as date, t.categ_id, m.product_tmpl_id, l.product_id as product_id, t.uom_id as product_uom, l.product_uom_qty, l.qty_received as qty_delivered, l.total_weight as order_weight, j.name as job_order, 0 as in_qty, 0 as out_qty, 0 as in_weight, 0 as out_weight, p.team_id, o.partner_id, o.company_id, o.user_id
from job_order j
join purchase_order o on o.job_order_id = j.id
join res_partner p on o.partner_id = p.id
join purchase_order_line l on l.order_id = o.id
join product_product m on l.product_id = m.id
join product_template t on m.product_tmpl_id = t.id
join product_category c on t.categ_id = c.id
left join res_company b on o.company_id = b.id
left join res_users u on o.user_id = u.id
left join crm_team r on p.team_id = r.id
where o.state in ('purchase','done')
union all
select o.id, s.global_ref, o.name as name,o.date_start as date, t.categ_id, m.product_tmpl_id, o.product_id as product_id, t.uom_id as product_uom, o.product_uom_qty, (o.product_uom_qty - o.product_qty) as qty_delivered, o.production_weight as order_weight, j.name as job_order, 0 as in_qty, 0 as out_qty, 0 as in_weight, 0 as out_weight, p.team_id, s.partner_id, o.company_id, o.user_id
from job_order j
join sale_order s on j.sale_id = s.id
join mrp_production o on o.job_order_id = j.id
join mrp_bom bm on o.bom_id = bm.id
join res_partner p on s.partner_id = p.id
join product_product m on o.product_id = m.id
join product_template t on m.product_tmpl_id = t.id
join product_category c on t.categ_id = c.id
left join res_company b on o.company_id = b.id
left join res_users u on o.user_id = u.id
left join crm_team r on p.team_id = r.id
where o.state not in ('draft','confirmed','planned','cancel') 
and bm.type = 'normal'
union all
select o.id, so.global_ref, o.reference as name, o.date, t.categ_id, m.product_tmpl_id, l.product_id as product_id, t.uom_id as product_uom, 0 as product_uom_qty, 0 as qty_delivered, 0 as order_weight, j.name as job_order, 
(case when ld.usage='internal' and ls.usage !='internal' then l.qty_done else 0 end) as in_qty, 
(case when ls.usage='internal' and ld.usage !='internal' then l.qty_done else 0 end) as out_qty,
(case when ld.usage='internal' and ls.usage !='internal' then l.total_weight else 0 end) as in_weight, 
(case when ls.usage='internal' and ld.usage !='internal' then l.total_weight else 0 end) as out_weight,
p.team_id, o.partner_id, o.company_id, pk.user_id
from stock_move o
join stock_move_line l on l.move_id = o.id
join stock_location ls on o.location_id = ls.id
join stock_location ld on o.location_dest_id = ld.id
left join stock_picking pk on o.picking_id =pk.id
left join sale_order so on l.sale_id = so.id
left join mrp_production mo on o.production_id = mo.id
left join job_order j on l.ref_job_order_id = j.id
left join res_partner p on o.partner_id = p.id
join product_product m on o.product_id = m.id
join product_template t on m.product_tmpl_id = t.id
join product_category c on t.categ_id = c.id
left join res_company b on o.company_id = b.id
left join res_users u on pk.user_id = u.id
left join crm_team r on p.team_id = r.id
where o.state = 'done'
) x
group by x.global_ref, x.name, x.date, x.categ_id, x.product_tmpl_id, x.product_id, x.product_uom,x.job_order,x.team_id,x.partner_id,x.company_id,x.user_id
"""

        for field in fields.values():
            select_ += field
        
        from_ = groupby_ = ''

        return '%s (SELECT %s %s %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))