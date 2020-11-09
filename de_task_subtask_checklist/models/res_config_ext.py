# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProjectResConfigSettingsExt(models.TransientModel):
    _inherit = 'res.config.settings'

    task_progress_restriction = fields.Selection([
        ('no_restriction', 'No Restriction to Task Progress'),
        ('progress_restriction', 'Restrict Task Progress Before All Checklist Completion')
    ], group_expand='_expand_states',
        track_visibility='onchange', help='Task Restriction')

    def set_values(self):
        super(ProjectResConfigSettingsExt, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("de_task_subtask_checklist.task_progress_restriction",
                                                         self.task_progress_restriction)

    @api.model
    def get_values(self):
        res = super(ProjectResConfigSettingsExt, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        task_progress_restriction = params.get_param('de_task_subtask_checklist.task_progress_restriction')
        res.update(
            task_progress_restriction=task_progress_restriction,
        )
        return res


class ProjectTaskTypeExt(models.Model):
    _inherit = 'project.task.type'

    @api.model
    def _get_default_progress_restriction(self):
        # for rec in self:
        default_progress_restriction = self.env['ir.config_parameter'].sudo().get_param('de_task_subtask_checklist.task_progress_restriction','False')
        return default_progress_restriction

    checklist_task_restrict = fields.Boolean(string='Checklist Task Progress Restriction')
    progress_restriction = fields.Selection([
        ('no_restriction', 'No Restriction to Task Progress'),
        ('progress_restriction', 'Restrict Task Progress Before All Checklist Completion')
    ], default=_get_default_progress_restriction)
