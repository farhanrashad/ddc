#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskSLA(models.Model):
    _name = "helpdesk.ticket.sla"
    _order = "name"
    _description = "Helpdesk SLA Policies"

    name = fields.Char('SLA Policy Name', required=True, index=True)
    description = fields.Text('SLA Policy Description')
    active = fields.Boolean('Active', default=True)
    team_id = fields.Many2one('helpdesk.ticket.team', 'Team', required=True)
    ticket_type_id = fields.Many2one(
        'helpdesk.ticket.type', "Ticket Type",
        help="Only apply the SLA to a specific ticket type. If left empty it will apply to all types.")
    stage_id = fields.Many2one(
        'helpdesk.ticket.stage', 'Target Stage', required=True,
        help='Minimum stage a ticket needs to reach in order to satisfy this SLA.')
    #priority = fields.Selection(TICKET_PRIORITY, string='Minimum Priority', default='0', required=True, help='Tickets under this priority will not be taken into account.')
    #company_id = fields.Many2one('res.company', 'Company', related='team_id.company_id', readonly=True, store=True)
    time_days = fields.Integer('Days', default=0, required=True, help="Days to reach given stage based on ticket creation date")
    time_hours = fields.Integer('Hours', default=0, required=True, help="Hours to reach given stage based on ticket creation date")

    @api.onchange('time_hours')
    def _onchange_time_hours(self):
        if self.time_hours >= 24:
            self.time_days += self.time_hours / 24
            self.time_hours = self.time_hours % 24