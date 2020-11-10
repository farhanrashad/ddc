# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    project_id = fields.Many2one("project.project", string="Project", domain="[('allow_timesheets', '=', True), ('company_id', '=', company_id)]")
        
    sale_id = fields.Many2one('sale.order',string='Sale Order', domain="[('company_id', '=', company_id)]")
    product_id = fields.Many2one('product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
    
    diagnosys_count = fields.Integer('diagnosys Count', compute='_compute_diagnosys_count', compute_sudo=True)
    diagnosys_ids = fields.One2many('project.task', 'ticket_id', string='diagnosys',  domain="[('is_diagnosys','=',True),('active','=',True),('project_id','=',project_id)]")
    
    workorder_count = fields.Integer('workorder Count', compute='_compute_workorder_count', compute_sudo=True)
    workorder_ids = fields.One2many('project.task', 'ticket_id', string='Work Orders', domain="[('is_workorder','=',True),('active','=',True),('project_id','=',project_id)]")

    @api.onchange('team_id')
    def onchange_team(self):
        for line in self:
            line.update({
                'project_id': line.team_id.project_id.id
            })
        
    @api.depends('diagnosys_ids')
    def _compute_diagnosys_count(self):
        for ticket in self:
            diagnosys_cnt = 0
            for order in ticket.diagnosys_ids:
                if order.active and order.is_diagnosys and order.project_id.id == ticket.project_id.id:
                    diagnosys_cnt += 1
            ticket.diagnosys_count = diagnosys_cnt

    def action_view_diagnosys(self):
        self.ensure_one()

        list_view_id = self.env.ref('project.view_task_tree2').id
        form_view_id = self.env.ref('project.view_task_form2').id

        action = {
            'type': 'ir.actions.act_window_close',
            'name': _('Diagnosys'),
            'domain': [('ticket_id', '=', self.id),('is_diagnosys','=',True)],
        }
        
        task_projects = self.diagnosys_ids.mapped('project_id')
        if len(task_projects) == 1 and len(self.diagnosys_ids) > 1:  # redirect to task of the project (with kanban stage, ...)
            action = self.with_context(active_id=task_projects.id).env.ref(
                'project.act_project_project_2_project_task_all').read()[0]
            if action.get('context'):
                eval_context = self.env['ir.actions.actions']._get_eval_context()
                eval_context.update({'active_id': task_projects.id})
                action['context'] = safe_eval(action['context'], eval_context)
        else:
            action = self.env.ref('project.action_view_task').read()[0]
            action['context'] = {}  # erase default context to avoid default filter
            if len(self.diagnosys_ids) > 1:  # cross project kanban task
                action['views'] = [[False, 'kanban'], [list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'calendar'], [False, 'pivot']]
            elif len(self.diagnosys_ids) == 1:  # single task -> form view
                action['views'] = [(form_view_id, 'form')]
                action['res_id'] = self.diagnosys_ids.id
        # filter on the task of the current SO
        action['domain'] = [('ticket_id', '=', self.id),('is_diagnosys','=',True)]
        action.setdefault('context', {})
        action['context'].update({'search_default_ticket_id': self.id, 'search_default_is_diagnosys': True })
        return action
    
    @api.depends('workorder_ids')
    def _compute_workorder_count(self):
        for ticket in self:
            workorder_cnt = 0
            for order in ticket.workorder_ids:
                if order.active and order.is_workorder and order.project_id.id == ticket.project_id.id:
                    workorder_cnt += 1
            ticket.workorder_count = workorder_cnt
            
            
        #workorder_data = self.env['project.task'].sudo().read_group([('ticket_id', 'in', self.ids),('is_workorder','=',True)], ['ticket_id'], ['ticket_id'])
        #mapped_data = dict([(r['ticket_id'][0], r['ticket_id_count']) for r in workorder_data])
        #for ticket in self:
            #ticket.workorder_count = mapped_data.get(ticket.id, 0)

    
    def action_view_workorder(self):
        self.ensure_one()

        list_view_id = self.env.ref('project.view_task_tree2').id
        form_view_id = self.env.ref('project.view_task_form2').id

        action = {
            'type': 'ir.actions.act_window_close',
            'name': _('Workorders'),
            'domain': [('ticket_id', '=', self.id),('is_workorder','=',True)],
        }
        
        task_projects = self.workorder_ids.mapped('project_id')
        if len(task_projects) == 1 and len(self.workorder_ids) > 1:  # redirect to task of the project (with kanban stage, ...)
            action = self.with_context(active_id=task_projects.id).env.ref(
                'project.act_project_project_2_project_task_all').read()[0]
            if action.get('context'):
                eval_context = self.env['ir.actions.actions']._get_eval_context()
                eval_context.update({'active_id': task_projects.id})
                action['context'] = safe_eval(action['context'], eval_context)
        else:
            action = self.env.ref('project.action_view_task').read()[0]
            action['context'] = {}  # erase default context to avoid default filter
            if len(self.workorder_ids) > 1:  # cross project kanban task
                action['views'] = [[False, 'kanban'], [list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'calendar'], [False, 'pivot']]
            elif len(self.workorder_ids) == 1:  # single task -> form view
                action['views'] = [(form_view_id, 'form')]
                action['res_id'] = self.workorder_ids.id
        # filter on the task of the current SO
        action['domain'] = [('ticket_id', '=', self.id),('is_workorder','=',True)]
        action.setdefault('context', {})
        action['context'].update({'search_default_ticket_id': self.id, 'search_default_is_workorder': True })
        return action
