# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class RepairWarrenty(models.Model):
    _inherit = 'repair.order'

    sale_warranty_id = fields.Many2one('sales.warranty', string="Sales Warranty", help="Sales Warranty")
    
    def action_repair_end(self):
        res = super(RepairWarrenty, self).action_repair_end()
        warranty_start_date = warranty_end_date = datetime.date.today()
        fees = self.env['repair.fee'].search([('repair_id', '=', self.id)])
        for line in fees:
            if line.is_warranty:
                if line.product_id.warranty_period == 'y':
                    warranty_end_date = warranty_start_date + datetime.timedelta(days=(line.product_id.warranty_period_interval*365))
                elif line.product_id.warranty_period == 'm':
                    warranty_end_date = warranty_start_date + datetime.timedelta(days=(line.product_id.warranty_period_interval*30))
                elif line.product_id.warranty_period == 'd':
                    warranty_end_date = warranty_start_date + datetime.timedelta(days=line.product_id.warranty_period_interval)
            
                vals = {
                    'product_id':line.product_id.id,
                    'partner_id':self.partner_id.id,
                    'repair_id':self.id,
                    'notes': 'Service Warranty',
                    'warranty_type':'service',
                    'purchase_date':warranty_start_date,
                    'warranty_start_date':warranty_start_date,
                    'warranty_end_date':warranty_end_date,
                    'state': 'draft',
                    'user_id':self.create_uid.id,
                }
                warranty_id = self.env['sales.warranty'].create(vals)
        
    
class RepairFeeWarrenty(models.Model):
    _inherit = 'repair.fee'
    
    def _default_warranty(self):
        return self.product_id.is_warranty
    
    is_warranty = fields.Boolean(string='Is Warranty',default='_default_warranty')