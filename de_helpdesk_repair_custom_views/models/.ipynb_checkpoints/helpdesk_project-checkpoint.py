# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskProjectTask(models.Model):
    _inherit = 'project.task'
    
    sap_no = fields.Char(related='ticket_id.sap_no', string='Order Number')
    crmid = fields.Char(related='ticket_id.crmid', string='CRMID')
    
    material = fields.Char(related='ticket_id.material', string='Equipment')
    partner_name = fields.Char(related='ticket_id.partner_name', string='Customer Name')
    contact_name = fields.Char(related='ticket_id.contact_name', string='Contact Name')
    contact_no = fields.Char(related='ticket_id.contact_no', string='Telephone')
    site_address = fields.Char(related='ticket_id.site_address', string='Street')
    ticket_description = fields.Text(related='ticket_id.description', string='Description')
    additional_info1 = fields.Text(related='ticket_id.additional_info1', string='Returned Equipment')
    distributor = fields.Char(related='ticket_id.distributor', string='distributor')
    address2 = fields.Text(related='ticket_id.address2', string='Long Text')
    city = fields.Char(related='ticket_id.city', string='City Name')
    notified_date = fields.Date(related='ticket_id.notified_date', string='Notification Date')
    receive_date = fields.Date(related='ticket_id.receive_date', string='Receive Date')
    user_id = fields.Many2one('res.users',related='ticket_id.user_id', string='Tech Name')
    
    barcode = fields.Char(related='ticket_id.barcode', string='Barcode')
    asset_no = fields.Char(related='ticket_id.asset_no', string='Asset Code')
    asset_model = fields.Char(related='ticket_id.asset_model', string='Asset Model')
    
    category_id = fields.Many2one('helpdesk.ticket.category',related='ticket_id.category_id', string='Main Category')
    ticket_tag_ids = fields.Many2many('helpdesk.ticket.tag',related='ticket_id.tag_ids', string='Sub Category')
    ticket_stage_id = fields.Many2one('helpdesk.ticket.stage',related='ticket_id.stage_id', string='Status')




    


