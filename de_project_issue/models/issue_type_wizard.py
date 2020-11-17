from odoo import models, fields, api


class IssueTypeWizard(models.TransientModel):
    _name = 'wizard.issue.type'
    _description = 'Issue Type'

    issue_title = fields.Char()
    assign_to = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)
    project_id = fields.Many2one('project.project')
    customer_id = fields.Many2one('res.partner')
    task_id = fields.Many2one('project.task')
    issue_type_id = fields.Many2one('project.issue.type')
    desc = fields.Html()
    environment = fields.Html()

    @api.onchange('company_id')
    def onchange_project(self):
        self.model = self.env.context.get('active_model')
        print(self.model)
        act_id = self.env[self.model].browse(self.env.context.get('active_id'))
        if self.model == 'project.project':
            self.project_id = act_id.id

        if self.model == 'project.task':
            self.project_id = act_id.project_id.id
            self.task_id = act_id.id
            self.assign_to = act_id.user_id.id

    def action_create_issue(self):
        link_id = 0
        self.model = self.env.context.get('active_model')
        print(self.model)
        act_id = self.env[self.model].browse(self.env.context.get('active_id'))

        if self.model == 'project.project':
            link_id = ''

        if self.model == 'project.task':
            link_id = act_id.id

        rec = self.env['project.task'].create({
            'name': self.issue_title,
            'user_id': self.assign_to.id,
            'company_id': self.company_id.id,
            'project_id': self.project_id.id,
            # 'customer_id': self.customer_id,
            'task_id': self.task_id.id,
            'issue_type': self.issue_type_id.id,
            'description': self.desc,
            'environment': self.environment,
            'is_issue': True,
            'issue_id': link_id,
        })
        return rec
