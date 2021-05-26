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
    _name = "report.de_sale_product_move_report.de_sale_stock_pdf_report"

    
    def _get_report_values(self, docids, data=None):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        query_param = ''
        
        if data['sale_id']:
            query_param = query_param + " and a.sale_id = %(sale_id)s "
        
        if data['partner_id']:
            query_param = query_param + " and a.partner_id = %(partner_id)s "
        

        cr = self._cr
        query = """
        select a.product_id, a.product_name,a.uom, a.location,a.lot, sum(a.quantity) as quantity, sum(a.product_weight) as product_weight from (
select l.product_id, pt.name as product_name, um.name as uom, m.partner_id, l.sale_id, sl.name as location, lot.name as lot, l.qty_done as quantity, coalesce(l.total_weight,0) as product_weight 
from stock_move m
join stock_move_line l on l.move_id = m.id
join product_product pp on l.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on l.location_dest_id = sl.id
left join stock_production_lot lot on l.lot_id = lot.id 
where m.state in ('done' ) and l.date <=  %(date)s and (l.location_dest_id = %(location_id)s or l.location_dest_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
union all
select l.product_id, pt.name as product_name, um.name as uom, m.partner_id, l.sale_id, sl.name as location, lot.name as lot, l.qty_done*-1 as quantity, coalesce(l.total_weight,0)*-1 as product_weight 
from stock_move m
join stock_move_line l on l.move_id = m.id
join product_product pp on l.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on l.location_id = sl.id
left join stock_production_lot lot on l.lot_id = lot.id 
where m.state in ('done' ) and l.date <=  %(date)s and (l.location_id = %(location_id)s or l.location_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
) a where a.location is not null """ + query_param + """
group by a.product_id, a.product_name,a.uom, a.location,a.lot
order by 1
        """ 
        query1 = """
        select a.product_id, a.product_name,a.uom, a.location, sum(a.quantity) as quantity, sum(a.product_weight) as product_weight from (
select l.product_id, pt.name as product_name, um.name as uom, m.partner_id, l.sale_id, sl.name as location, lot.name as lot, l.qty_done as quantity, coalesce(l.total_weight,0) as product_weight 
from stock_move m
join stock_move_line l on l.move_id = m.id
join product_product pp on l.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on l.location_dest_id = sl.id
left join stock_production_lot lot on l.lot_id = lot.id 
where m.state in ('done' ) and l.date <=  %(date)s and (l.location_dest_id = %(location_id)s or l.location_dest_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
union all
select l.product_id, pt.name as product_name, um.name as uom, m.partner_id, l.sale_id, sl.name as location, lot.name as lot, l.qty_done*-1 as quantity, coalesce(l.total_weight,0)*-1 as product_weight 
from stock_move m
join stock_move_line l on l.move_id = m.id
join product_product pp on l.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on l.location_id = sl.id
left join stock_production_lot lot on l.lot_id = lot.id 
where m.state in ('done' ) and l.date <=  %(date)s and (l.location_id = %(location_id)s or l.location_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
) a where a.location is not null """ + query_param + """
group by a.product_id, a.product_name,a.uom, a.location
order by 1
        """ 

        query2 = """
        select a.product_category, max(a.uom) as uom, a.location, sum(a.quantity) as quantity, sum(a.product_weight) as product_weight from (
select l.product_id, pt.name as product_name, um.name as uom, pt.categ_id, pc.name as product_category, m.partner_id, l.sale_id, sl.name as location, lot.name as lot, l.qty_done as quantity, coalesce(l.total_weight,0) as product_weight 
from stock_move m
join stock_move_line l on l.move_id = m.id
join product_product pp on l.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join product_category pc on pt.categ_id = pc.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on l.location_dest_id = sl.id
left join stock_production_lot lot on l.lot_id = lot.id 
where m.state in ('done' ) and l.date <=  %(date)s and (l.location_dest_id = %(location_id)s or l.location_dest_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
union all
select l.product_id, pt.name as product_name, um.name as uom, pt.categ_id, pc.name as product_category, m.partner_id, l.sale_id, sl.name as location, lot.name as lot, l.qty_done*-1 as quantity, coalesce(l.total_weight,0)*-1 as product_weight 
from stock_move m
join stock_move_line l on l.move_id = m.id
join product_product pp on l.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
join product_category pc on pt.categ_id = pc.id
join uom_uom um on pt.uom_id = um.id
join stock_location sl on l.location_id = sl.id
left join stock_production_lot lot on l.lot_id = lot.id 
where m.state in ('done' ) and l.date <=  %(date)s and (l.location_id = %(location_id)s or l.location_id in (select z.id from stock_location z where z.location_id = %(location_id)s ) )
) a where a.location is not null """ + query_param + """
group by a.product_category, a.location
order by 1
        """ 

        
        params = {'date': data['date'], 'sale_id':data['sale_id'],'location_id':data['location_id'],'partner_id':data['partner_id']}

        self.env.cr.execute(query, params=params)        
        dat = cr.dictfetchall()
        
        self.env.cr.execute(query1, params=params) 
        dat1 = cr.dictfetchall()
        
        self.env.cr.execute(query2, params=params) 
        dat2 = cr.dictfetchall()

        return {
            'doc_ids': self.ids,
            'doc_model': 'sale.stock',
            'dat': dat,
            'dat1': dat1,
            'dat2': dat2,
            'data': data,
            'docs': docs
        }
