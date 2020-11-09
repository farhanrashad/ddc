# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class TaskChecklist(models.Model):
    _name = 'task.checklist'
    _rec_name = 'name'
    _description = 'Task Checklist'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    checklist_ids = fields.One2many(comodel_name='task.checklist.line', inverse_name='checklist_id')


class TaskChecklistLine(models.Model):
    _name = 'task.checklist.line'
    _description = 'Task Checklist Line'

    checklist_id = fields.Many2one(comodel_name='task.checklist')
    activity_id = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    task_id = fields.Many2one(comodel_name='project.task', string='Task')
