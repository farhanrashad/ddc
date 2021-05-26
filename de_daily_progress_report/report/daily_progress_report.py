# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#################################################################################

import time
from odoo import api, models
from dateutil.parser import parse
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class DailyProgressReport(models.AbstractModel):
    _name = 'report.de_daily_progress_report.progress_report_template'

    '''Find Purchase invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self, docids, data=None):       
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        outstanding_invoice = []       
        doc_date = docs.date + timedelta(hours=0) 
        docs_date = docs.date + timedelta(hours=1) 
        lot_records = self.env['stock.move.line'].search([('date','>=',doc_date),('date','<=',docs_date)])
        mrp_production = self.env['mrp.production'].search([('date_planned_start', '=', docs.date),
                                                          ])


        if lot_records:
             return {
                'docs': docs,
                 'lot_records': lot_records,
                 'mrp_production': mrp_production,
             }
        else:
            raise UserError("There is not any Record between selected date")

            
    
