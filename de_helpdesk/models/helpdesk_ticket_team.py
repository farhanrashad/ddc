from odoo import api, fields, models


class HelpdeskTeam(models.Model):

    _name = 'helpdesk.ticket.team'
    _description = 'Helpdesk Ticket Team'

    name = fields.Char(string='Name', required=True)
    user_ids = fields.Many2many(comodel_name='res.users', string='Members')
    active = fields.Boolean(default=True)
    category_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.category',
        string='Category')
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'helpdesk.ticket')
    )

    color = fields.Integer("Color Index", default=0)

    ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'team_id',
        string="Tickets")

    todo_ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'team_id',
        string="Todo tickets")

    todo_ticket_count = fields.Integer(
        string="Number of tickets",
        compute='_compute_todo_tickets')

    todo_ticket_count_unassigned = fields.Integer(
        string="Number of tickets unassigned",
        compute='_compute_unassigned_tickets')

    todo_ticket_count_unattended = fields.Integer(
        string="Number of tickets unattended",
        compute='_compute_todo_tickets')

    todo_ticket_count_high_priority = fields.Integer(
        string="Number of tickets in high priority",
        compute='_compute_todo_tickets')

    def _compute_unassigned_tickets(self):
        ticket_data = self.env['helpdesk.ticket'].read_group([('user_id', '=', False), ('team_id', 'in', self.ids), ('stage_id.closed', '!=', True)], ['team_id'], ['team_id'])
        mapped_data = dict((data['team_id'][0], data['team_id_count']) for data in ticket_data)
        for team in self:
            team.todo_ticket_count_unassigned = mapped_data.get(team.id, 0)
            
    @api.depends('ticket_ids', 'ticket_ids.stage_id')
    def _compute_todo_tickets(self):
        #for ticket in self.ticket_ids:
        self.todo_ticket_count = 0
        #self.todo_ticket_count_unassigned = 0
        self.todo_ticket_count_unattended = 0
        self.todo_ticket_count_high_priority = 0
        #for record in self:
         #   record.todo_ticket_ids = record.ticket_ids.filtered(
          #      lambda ticket: not ticket.closed)
           # record.todo_ticket_count = len(record.todo_ticket_ids)
            #record.todo_ticket_count_unassigned = len(
             #   record.todo_ticket_ids.filtered(
              #      lambda ticket: not ticket.user_id))
            #record.todo_ticket_count_unattended = len(
             #   record.todo_ticket_ids.filtered(
              #      lambda ticket: ticket.unattended))
            #record.todo_ticket_count_high_priority = len(
             #   record.todo_ticket_ids.filtered(
              #      lambda ticket: ticket.priority == '3'))
