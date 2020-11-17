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

    unassigned_tickets = fields.Integer(
        string="Number of tickets unassigned",
        compute='_compute_unassigned_tickets')

    unattended_tickets = fields.Integer(
        string="Number of tickets unattended",
        compute='_compute_unattended_tickets')

    high_priority_tickets = fields.Integer(
        string="Number of tickets in high priority",
        compute='_compute_high_priority_tickets')

    def _compute_unassigned_tickets(self):
        ticket_data = self.env['helpdesk.ticket'].read_group([('user_id', '=', False), ('team_id', 'in', self.ids), ('stage_id.closed', '=', False)], ['team_id'], ['team_id'])
        mapped_data = dict((data['team_id'][0], data['team_id_count']) for data in ticket_data)
        for team in self:
            team.unassigned_tickets = mapped_data.get(team.id, 0)
            
    def _compute_todo_tickets(self):
        ticket_data = self.env['helpdesk.ticket'].read_group([('team_id', 'in', self.ids), ('stage_id.closed', '=', False)], ['team_id'], ['team_id'])
        mapped_data = dict((data['team_id'][0], data['team_id_count']) for data in ticket_data)
        for team in self:
            team.todo_ticket_count = mapped_data.get(team.id, 0)
    
    def _compute_unattended_tickets(self):
        ticket_data = self.env['helpdesk.ticket'].read_group([('team_id', 'in', self.ids), ('stage_id.unattended', '=', True)], ['team_id'], ['team_id'])
        mapped_data = dict((data['team_id'][0], data['team_id_count']) for data in ticket_data)
        for team in self:
            team.unattended_tickets = mapped_data.get(team.id, 0)
    
    def _compute_high_priority_tickets(self):
        ticket_data = self.env['helpdesk.ticket'].read_group([('team_id', 'in', self.ids), ('priority', '=', 2)], ['team_id'], ['team_id'])
        mapped_data = dict((data['team_id'][0], data['team_id_count']) for data in ticket_data)
        for team in self:
            team.high_priority_tickets = mapped_data.get(team.id, 0)          
            
    