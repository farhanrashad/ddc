from odoo import models, fields, api


class ProjectIssueType(models.Model):
    _name = 'project.issue.type'

    name = fields.Char(string="Type Name", required=True)


class IssueType(models.Model):
    _inherit = 'project.task'

    is_issue = fields.Boolean(Default=False, string='Issue?')
    issue_type = fields.Many2one('project.issue.type', string='Issue Type')
    issue_type_count = fields.Integer(compute='_project_issue_count_all')
    task_id = fields.Char(string='Task')
    environment = fields.Html()
    issue_lines = fields.One2many('project.task', 'issue_id')
    issue_id = fields.Many2one('project.task')

    def _project_issue_count_all(self):
        for record in self:
            record.issue_type_count = self.env['project.task'].search_count([('issue_id', '=', record.id), ('is_issue', '=', True)])


class ProjectIssue(models.Model):
    _inherit = 'project.project'

    issue_type_count = fields.Integer(compute='_project_issue_count_all')
    is_issue = fields.Boolean(Default=False, string='Issue?')

    def _project_issue_count_all(self):
        for record in self:
            record.issue_type_count = self.env['project.task'].search_count(
                [('is_issue', '=', True), ('project_id', '=', record.id)])
