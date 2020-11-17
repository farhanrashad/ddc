# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTaskSecurity(models.Model):
    _name = 'project.task.security'
    _description = 'de project security'

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        project_id = self.env.context.get('default_project_id')
        if not project_id:
            return False
        return self.stage_find(project_id, [('fold', '=', False)])

    name = fields.Char()
    value = fields.Integer()
    stage_id = fields.Many2one('project.task.type', string='Stage', ondelete='restrict', tracking=True, index=True,
                               default=_get_default_stage_id, group_expand='_read_group_stage_ids',
                               domain="[('project_ids', '=', project_id)]", copy=False)
