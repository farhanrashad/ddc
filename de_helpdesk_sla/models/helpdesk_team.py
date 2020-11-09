#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket.team"
    
    resource_calendar_id = fields.Many2one('resource.calendar', 'Working Hours', default=lambda self: self.env.company.resource_calendar_id, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    use_sla = fields.Boolean('SLA Policies')
