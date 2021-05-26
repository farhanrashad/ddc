# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'
        
    production_status = fields.Char(string='Production Status', help="Calculate Production Status")
    
    
    def _compute_production_status(self):
        for line in self:
            aml_obj = self.env['mrp.production']
            domain = [('ref_sale_id', '=', line.id),]
            where_query = aml_obj._where_calc(domain)
            aml_obj._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT max(state) from " + from_clause + " where " + where_clause

            self.env.cr.execute(select, where_clause_params)
            line.production_status = self.env.cr.fetchone()[0] or ''
            
    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()        
        self.update({
            'production_status': 'Pending'
        })
        return res
    
    def action_cancel(self):
        res = super(SaleOrder,self).action_cancel()        
        self.update({
            'production_status': 'Cancelled'
        })
        return res