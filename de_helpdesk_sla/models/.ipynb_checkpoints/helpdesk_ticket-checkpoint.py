#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"
    
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', "Ticket Type", help="Only apply the SLA to a specific ticket type. If left empty it will apply to all types.")
    
    sla_deadline_date = fields.Date('Deadline')
    
    total_time_spent = fields.Date('Total Time Spent')
    
    