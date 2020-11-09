# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProjectTaskStageExt(models.Model):
    _inherit = 'project.task.type'

    user_id = fields.Many2one(comodel_name='res.users', string='Default Assigned User')
    default_for_new_proj = fields.Boolean(string='Default for new Project')
