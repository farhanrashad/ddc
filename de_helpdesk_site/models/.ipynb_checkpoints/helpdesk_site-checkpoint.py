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
    
    address2 = fields.Text('Long Text')
    
    reference = fields.Char('Reference')
    
    material = fields.Char('Material')
    barcode = fields.Char('Barcode/Serial')
    asset_no = fields.Char('Asset No.')
    asset_model = fields.Char('Asset Model')
    
    customer_model_desc = fields.Char('Customer Model Desc')
    reason = fields.Text('Reason')
    crmid = fields.Char('CRM ID')
    sap_no = fields.Char('SAP No.')
    
    receive_date = fields.Date('Receiving Date')
    notified_date = fields.Date('Notification Date')
    
    additional_info1 = fields.Text('Return Equipment Remarks')
    additional_info2 = fields.Text('Additional Requirement')
    
    @api.constrains('name', 'stage_id')
    def _check_unique_sequence_number(self):
        moves = self.filtered(lambda move: move.stage_id.name == 'posted')
        if not moves:
            return
        self.flush()