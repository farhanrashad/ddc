# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime


class HelpdeskTicketSlaInh(models.Model):
    _inherit = 'helpdesk.ticket.sla'
    
    team_ids = fields.Many2many('helpdesk.ticket.team')
    team_id = fields.Many2one('helpdesk.ticket.team', required=False)
    


class HelpdeskTicketInh(models.Model):
    _inherit = 'helpdesk.ticket'
    
    sla_ids = fields.Many2many('helpdesk.ticket.sla', string="SLA", compute='_compute_helpdesk_ticket_sla', store=True)
    sla_status = fields.Char('Achieved', compute='get_status')
    sla_status_lines = fields.One2many('sla.status.line', 'ticket_id')
    description = fields.Text('Descriptions')


    @api.depends('team_id')
    def _compute_helpdesk_ticket_sla(self):
        for ticket in self:
            record = self.env['helpdesk.ticket.sla'].search([])
            my_list = []
            for rec in record:
                if ticket.team_id in rec.team_ids:
                    my_list.append(rec.id)
            ticket.sla_ids = my_list
            for line in ticket.sla_status_lines:
                line.unlink()
            if ticket.create_date:
                date = ticket.create_date
            else:
                date = datetime.today().date()
        
            for level in ticket.sla_ids:     
                self.env['sla.status.line'].create({
                'ticket_id': ticket.id,
                'name': level.name,
                'completion_date': date + relativedelta(days=level.time_days),
                'completion_stage': level.stage_id.id,   
              })

#     @api.onchange('team_id')
#     def get_levels(self):
#         record = self.env['helpdesk.ticket.sla'].search([])
#         my_list = []
#         for rec in record:
#             if self.team_id in rec.team_ids:
#                 my_list.append(rec.id)
#         self.sla_ids = my_list
        
#         for line in self.sla_status_lines:
#             line.unlink()
#         if self.create_date:
#             date = self.create_date
#         else:
#             date = datetime.today().date()
        
#         for level in self.sla_ids:     
#             self.env['sla.status.line'].create({
#                 'ticket_id': self.id,
#                 'name': level.name,
#                 'completion_date': date + relativedelta(days=level.time_days),
#                 'completion_stage': level.stage_id.id,   
#             })
            
    @api.onchange('stage_id')
    def compute_level_dates(self):
        if self.stage_id.name == 'Settled':
            for rec in self.sla_status_lines:
                if datetime.today().date() <= rec.completion_date:
                    rec.sla_status = 'successful'
                    break
                else:
                    rec.sla_status = 'failed'
    

    def get_status(self):
        if self.sla_status_lines:
            for rec in self.sla_status_lines:
                if rec.sla_status == 'successful':
                    Line_id = rec.id
                    break
                else:
                    Line_id = -1
            if Line_id != -1:
                line = self.env['sla.status.line'].browse([Line_id])
                self.sla_status = line.name
            else:
                self.sla_status = "Failed"

        else:
            self.sla_status = "Failed"
        
class SlaStatusLine(models.Model):
    _name = 'sla.status.line'
    
    ticket_id = fields.Many2one('helpdesk.ticket')
    name = fields.Char('Level')
    completion_date = fields.Date('Reach Date')
    completion_stage = fields.Many2one('helpdesk.ticket.stage', string='Action Stage')
    sla_status = fields.Selection([
        ('successful', 'Successfull'),
        ('failed', 'Failed'),
        ], string='SLA Status', index=True, copy=False, default='', track_visibility='onchange')


class HelpdeskProjectTask(models.Model):
    _inherit = 'project.task'

    sap_no = fields.Char(related='ticket_id.name', string='Order Number')
    crmid = fields.Char(related='ticket_id.crmid', string='CRMID')

    material = fields.Char(related='ticket_id.material', string='Equipment')
    partner_name = fields.Char(related='ticket_id.partner_name', string='Customer Name')
    contact_name_ticket = fields.Char(related='ticket_id.contact_name', string='Contact Name')
    contact_name = fields.Char(string='Contact Name')
    contact_no_ticket = fields.Char(related='ticket_id.contact_no', string='Telephone')
    contact_no = fields.Char(string='Telephone')
    site_address = fields.Char(related='ticket_id.site_address', string='Street')
    ticket_description = fields.Text(related='ticket_id.description', string='Description')
    additional_info1 = fields.Text(related='ticket_id.additional_info1', string='Returned Equipment')
    distributor = fields.Char(related='ticket_id.distributor', string='distributor')
    address2 = fields.Text(related='ticket_id.address2', string='Long Text')
    city = fields.Char(related='ticket_id.city', string='City Name')
    notified_date = fields.Date(related='ticket_id.notified_date', string='Notification Date')
    receive_date = fields.Date(related='ticket_id.receive_date', string='Receive Date')
    user_id = fields.Many2one('res.users', related='ticket_id.user_id', string='Tech Name')
    site_name = fields.Char('Site Name', related='ticket_id.site_name')
    closed_date = fields.Datetime('Closed Date', related='ticket_id.closed_date')
#     level = fields.Char('level', related='ticket_id.level')

    barcode = fields.Char(related='ticket_id.barcode', string='Barcode')
    asset_no = fields.Char(related='ticket_id.asset_no', string='Asset Code')
    asset_model = fields.Char(related='ticket_id.asset_model', string='Asset Model')

    category_id = fields.Many2one('helpdesk.ticket.category', related='ticket_id.category_id', string='Main Category')
    ticket_tag_ids = fields.Many2many('helpdesk.ticket.tag', related='ticket_id.tag_ids', string='Sub Category')
    ticket_stage_id = fields.Many2one('helpdesk.ticket.stage', related='ticket_id.stage_id', string='Status')


class HelpdeskProjectTask(models.Model):
    _inherit = 'project.task.planning.line'
    
    task_id = fields.Many2one('project.task', string='Task', index=True, required=True, ondelete='cascade')
    ticket_id = fields.Many2one('helpdesk.ticket', related='task_id.ticket_id', string='Ticket')
    sap_no = fields.Char(related='ticket_id.name', string='Order Number')
    city = fields.Char(related='ticket_id.city', string='City Name')
    asset_model = fields.Char(related='ticket_id.asset_model', string='Asset Model')
    ticket_stage_id = fields.Many2one('helpdesk.ticket.stage', related='ticket_id.stage_id', string='Status')
    material = fields.Char(related='ticket_id.material', string='Equipment')
    # default_code = fields.Char(related='product_id.default_code', string='Material Code')
    total_amount = fields.Float('Amount', compute='_calculate_amount')
    warranty_status = fields.Char("Warranty Status")
    date_deadline = fields.Datetime('Deadline', compute="get_date")
    material_code = fields.Char('Material Code')
    
    def get_date(self):
        for rec in self:
            rec.date_deadline = rec.task_id.date_deadline

    @api.depends('product_uom_qty', 'price_unit')
    def _calculate_amount(self):
        for line in self:
            line.total_amount = line.product_uom_qty * line.price_unit
