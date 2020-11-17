from odoo import models, fields, api
from odoo.exceptions import UserError


class ProjectTaskNew(models.Model):
    _inherit = 'project.task'

    is_revision = fields.Boolean(Default=False)
    revision_lines = fields.One2many('project.task', 'revision_id')
    revision_id = fields.Many2one('project.task')
    revision_req_count = fields.Integer(compute="_compute_request_count_all")

    def _compute_request_count_all(self):
        for record in self:
            record.revision_req_count = self.env['project.task'].search_count([('revision_id', '=', record.id), ('is_revision', '=', True)])

    def revision_action(self):
        # raise UserError("Revision Button is Pressed")
        project_task = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.project_id.id,
            'user_id': self.user_id.id,
            'date_deadline': self.date_deadline,
            'tag_ids': self.tag_ids,
            'is_revision': True,
            'revision_id': self.id,
        })

        form_id = self.env.ref('project.view_task_form2', False)
        return {
            'name': 'Project Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.task',
            'view_id': form_id.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': project_task.id,
            'context': {'force_detailed_view': 'true'},

        }


