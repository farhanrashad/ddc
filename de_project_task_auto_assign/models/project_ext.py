# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProjectProjectExt(models.Model):
    _inherit = 'project.project'

    auto_assign_ids = fields.One2many(comodel_name='task.assign', inverse_name='auto_assign_id')


class TaskAutoAssign(models.Model):
    _name = 'task.assign'
    _description = 'Project Task Auto Assign'

    auto_assign_id = fields.Many2one(comodel_name='project.project')
    stage_id = fields.Many2one(comodel_name='project.task.type', string='Stage', required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='User')


class ProjectTaskExt(models.Model):
    _inherit = 'project.task'

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for rec in self:
            project_id = self.env['project.project'].search([('id', '=', rec.project_id.id)])
            auto_assign = self.env['task.assign'].search(
                [('auto_assign_id', '=', project_id.id), ('stage_id', '=', rec.stage_id.id)])
            if auto_assign:
                rec.user_id = auto_assign.user_id.id
            else:
                st = self.env['project.task.type'].search([('id', '=', rec.stage_id.id)])
                if st.default_for_new_proj == True:
                    rec.user_id = st.user_id.id
