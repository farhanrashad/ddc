#-*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.osv import expression
from odoo.exceptions import AccessError
from odoo.osv import expression

from datetime import datetime, timedelta

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"
    
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', "Ticket Type", help="Only apply the SLA to a specific ticket type. If left empty it will apply to all types.")
    
    helpdesk_sla_id = fields.Many2one('helpdesk.ticket.sla', "Ticket SLA", help="Only apply the SLA to a specific ticket type. If left empty it will apply to all types.")
    sla_status_ids = fields.One2many('helpdesk.ticket.sla.status', 'ticket_id', string="SLA Status")
    sla_log_ids = fields.One2many('helpdesk.ticket.sla.log', 'ticket_id', string="SLA Log")
    deadline_date = fields.Datetime(string='Deadline Date', readonly=True, compute='_compute_deadline')
    
    def _compute_deadline1(self):
        sla_ids = self.env['helpdesk.ticket.sla'].search([('team_id','=',self.team_id.id),('active','=',True)])
        deadline_date = fields.Datetime.now()
        for sla in sla_ids:
            deadline_date = self.create_date + timedelta(days=sla.time_days)
            
        self.update({
            'deadline_date': deadline_date
        })
        
    @api.depends('create_date', 'helpdesk_sla_id')
    def _compute_deadline(self):
        for status in self:
            deadline = status.create_date
            working_calendar = status.team_id.resource_calendar_id

            if not working_calendar:
                status.deadline_date = deadline
                continue

            if status.helpdesk_sla_id.time_days > 0:
                deadline = working_calendar.plan_days(status.helpdesk_sla_id.time_days + 1, deadline, compute_leaves=True)
                # We should also depend on ticket creation time, otherwise for 1 day SLA, all tickets
                # created on monday will have their deadline filled with tuesday 8:00
                create_dt = status.create_date
                deadline = deadline.replace(hour=create_dt.hour, minute=create_dt.minute, second=create_dt.second, microsecond=create_dt.microsecond)

            # We should execute the function plan_hours in any case because, in a 1 day SLA environment,
            # if I create a ticket knowing that I'm not working the day after at the same time, ticket
            # deadline will be set at time I don't work (ticket creation time might not be in working calendar).
            status.deadline_date = working_calendar.plan_hours(status.helpdesk_sla_id.time_hours, deadline, compute_leaves=True)

    @api.model
    def create(self, vals):
        self._sla_log()
        res = super(HelpdeskTicket,self).create(vals)
        return res
    
    def _sla_log(self, cr, uid, ids, context=None):
        old_stage_id = self.browse(cr, uid, ids[0]).stage_id.id
        for log in self.sla_status_ids:
            log.create({
                'stage_id':self.stage_id.id,
                'start_on': fields.Datetime.now(),
                'end_on': fields.Datetime.now(),
            })
    
class HelpdeskSLAStatus(models.Model):
    _name = "helpdesk.ticket.sla.status"
    _description = "Helpdesk SLA Status"
    
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', required=True, ondelete='cascade', index=True)
    helpdesk_sla_id = fields.Many2one('helpdesk.ticket.sla', required=True, ondelete='cascade')
    stage_id = fields.Many2one('helpdesk.ticket.stage', related='helpdesk_sla_id.stage_id', store=True)  # need to be stored for the search in `_sla_reach`
    deadline = fields.Datetime("Deadline", compute='_compute_deadline', compute_sudo=True, store=True)
    reached_datetime = fields.Datetime("Reached Date", help="Datetime at which the SLA stage was reached for the first time")
    status = fields.Selection([('failed', 'Failed'), ('reached', 'Reached'), ('ongoing', 'Ongoing')], string="Status", compute='_compute_status', compute_sudo=True, search='_search_status')
    color = fields.Integer("Color Index", compute='_compute_color')
    exceeded_days = fields.Float("Excedeed Working Days", compute='_compute_exceeded_days', compute_sudo=True, store=True, help="Working days exceeded for reached SLAs compared with deadline. Positive number means the SLA was eached after the deadline.")
    
class HelpdeskSLALog(models.Model):
    _name = "helpdesk.ticket.sla.log"
    _description = "Helpdesk SLA log"
    
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', required=True, ondelete='cascade', index=True)
    stage_id = fields.Many2one('helpdesk.ticket.stage', store=True)  # need to be stored for the search in `_sla_reach`
    start_on = fields.Datetime("Start On", compute='_compute_deadline', compute_sudo=True, store=True)
    end_on = fields.Datetime("End On", help="Datetime at which the SLA stage was reached for the first time")    
    
    
    