#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskSite(models.Model):
    _inherit = "helpdesk.ticket"

    distributor = fields.Char('Distributor', index=True)
    site_name = fields.Char('Site Name', index=True)
    contact_name = fields.Char('Contact Name')
    contact_no = fields.Char('Contact no')
    site_address = fields.Char('Site Address')
    
    city = fields.Char('City')
    
    reference = fields.Char('Reference')
    
    material = fields.Char('Material')
    barcode = fields.Char('Barcode/Serial')
    model = fields.Char('Model')
    
    customer_model_desc = fields.Char('Customer Model Desc')
    reason = fields.Text('Reason')
    crmid = fields.Char('CRM ID')
    
    @api.constrains('name', 'stage_id')
    def _check_unique_sequence_number(self):
        moves = self.filtered(lambda move: move.stage_id.name == 'posted')
        if not moves:
            return
        self.flush()