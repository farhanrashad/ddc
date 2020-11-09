# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ProjectTaskExt(models.Model):
    _inherit = 'project.task'

    def _get_checklist_activity_progress(self):
        progress_value = 0.0
        progress = self.env['project.task.type'].search([('name', '=', 'Completed')])
        for rec in self:
            for item in rec.task_checklist_ids:
                if item.stage_id.id == progress.id:
                    progress_value += 10
            rec.activity_progress = progress_value

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for rec in self:
            final_id = self.env['project.task.type'].search(
                ['|', ('name', '=', 'Completed'), ('name', '=', 'Cancelled')])
            for line in rec.task_checklist_ids:
                if line.stage_id not in final_id:
                    if line.stage_id.checklist_task_restrict == True:
                        msg = _(
                            'You Can Not Change Stage To %s Because Some Activities are Not '
                            'In Completed or Cancelled Stage. \n') % (
                                  rec.stage_id.name)
                        raise UserError(msg)

    @api.onchange('checklist_id')
    def _onchange_checklist_id(self):
        for rec in self:
            rec.task_checklist_ids.unlink()
            checklist = self.env['task.checklist'].search([('id', '=', rec.checklist_id.id)])
            checklist_line = self.env['task.checklist.line'].search([('checklist_id', '=', checklist.id)])
            if checklist_line:
                for line in checklist_line:
                    rec.task_checklist_ids |= rec.task_checklist_ids.new({
                        'name': line.activity_id,
                        'description': line.description,
                    })

    checklist_id = fields.Many2one(comodel_name='task.checklist', string='Checklist',
                                   domain="[('project_id', '=', project_id)]")
    task_checklist_ids = fields.One2many(comodel_name='checklist.activity', inverse_name='task_checklist_id')
    activity_progress = fields.Float(string='Checklist Progress', compute='_get_checklist_activity_progress',
                                     default=0.0)
    max_rate = fields.Integer(string='Maximum rate', default=100)


class ChecklistActivities(models.Model):
    _name = 'checklist.activity'
    _rec_name = 'name'
    _description = 'Checklist Activity'

    def approve_button(self):
        for rec in self:
            approve_stage = self.env['project.task.type'].search([('name', '=', 'Done')], limit=1)
            rec.stage_id = approve_stage.id

    def mark_complete_button(self):
        for rec in self:
            completed_stage = self.env['project.task.type'].search([('name', '=', 'Completed')], limit=1)
            rec.stage_id = completed_stage.id

    def mark_cancel_button(self):
        for rec in self:
            canceled_stage = self.env['project.task.type'].search([('name', '=', 'Cancelled')], limit=1)
            rec.stage_id = canceled_stage.id

    task_checklist_id = fields.Many2one(comodel_name='project.task', string='Task Checklist Id')
    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    approve_user_id = fields.Many2one(comodel_name='res.users', string='Approve User')
    stage_id = fields.Many2one(comodel_name='project.task.type', string='Stage')
    task_id = fields.Many2one(comodel_name='project.task', string='Task')
    name_stage = fields.Char(string='Stage Name', related='stage_id.name', readonly=True)
