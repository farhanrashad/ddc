# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################
import pytz
import time

from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime


class CustomReport(models.AbstractModel):
    _name = "report.de_sale_stock_report.de_sale_stock_pdf_report"

    
    def _get_report_values(self, docids, data=None):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        query_param = ''
        
        if data['sale_id']:
            query_param = query_param + " and a.state in ('posted') "
        else:
            query_param = query_param + " and a.state in ('draft','posted') "

        cr = self._cr
        query = """
        select a.product_id, a.product_name,a.uom, a.location,a.lot, sum(a.quantity) as quantity, sum(a.product_weight) as product_weight from (
select q.product_id, pt.name as product_name, um.name as uom, sl.name as location, lot.name as lot, q.quantity, coalesce(q.product_weight,0) as product_weight 
from stock_quant q
join product_product pp on q.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on q.location_id = sl.id
left join stock_production_lot lot on q.lot_id = lot.id
where q.in_date <=  %(date)s and (q.location_id = %(location_id)s or q.location_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
and q.product_id in (
select l.product_id from sale_order s join sale_order_line l on l.order_id = s.id where s.id = %(sale_id)s
union
select l.product_id from purchase_order p join purchase_order_line l on l.order_id = p.id where p.sale_id = %(sale_id)s
union
select m.product_id from mrp_production m where m.ref_sale_id = %(sale_id)s
)
) a 
group by a.product_id, a.product_name,a.uom, a.location,a.lot
order by 1
        """ 
        query1 = """
        select a.product_id, a.product_name,a.uom, a.location, sum(a.quantity) as quantity, sum(a.product_weight) as product_weight from (
select q.product_id, pt.name as product_name, um.name as uom, sl.name as location, lot.name as lot, q.quantity, coalesce(q.product_weight,0) as product_weight 
from stock_quant q
join product_product pp on q.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on q.location_id = sl.id
left join stock_production_lot lot on q.lot_id = lot.id
where q.in_date <=  %(date)s and (q.location_id = %(location_id)s or q.location_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
and q.product_id in (
select l.product_id from sale_order s join sale_order_line l on l.order_id = s.id where s.id = %(sale_id)s
union
select l.product_id from purchase_order p join purchase_order_line l on l.order_id = p.id where p.sale_id = %(sale_id)s
union
select m.product_id from mrp_production m where m.ref_sale_id = %(sale_id)s
)
) a 
group by a.product_id, a.product_name,a.uom, a.location
order by 1
        """ 
        
        params = {'date': data['date'], 'sale_id':data['sale_id'],'location_id':data['location_id']}

        self.env.cr.execute(query, params=params)        
        dat = cr.dictfetchall()
        
        self.env.cr.execute(query1, params=params)        
        dat1 = cr.dictfetchall()

        return {
            'doc_ids': self.ids,
            'doc_model': 'sale.stock',
            'dat': dat,
            'dat1': dat1,
            'data': data,
            'docs': docs
        }
