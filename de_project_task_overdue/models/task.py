from odoo import models ,fields
from odoo.exceptions import UserError
import datetime
from datetime import timedelta
class ProjectTaskInherit(models.Model):

    _inherit = 'project.project'

    is_notify = fields.Boolean(string="Send notification")
    notify_day = fields.Char(string="Set days")

    def action_send_email(self):
           print("enter in action send email")
           list = []
           task_ids = self.env['project.task'].search([('project_id','=',self.id)])
           for task_id in task_ids:
               if task_id.date_deadline:
                   dead_line_date = task_id.date_deadline
                   current_date = datetime.date.today()
                   ultimate_dead_line = dead_line_date+timedelta(days=int(self.notify_day))
                   if current_date == ultimate_dead_line:
                        print("====all task=====", task_id.name)
                        list.append(task_id)
           employee_ids = self.env['hr.employee'].search([])
           if list:
               single_employee = []
               for employee_id in employee_ids:
                   for task_id in list:
                       user_email = task_id.user_id.login
                       if employee_id.id == task_id.user_id.id:
                               single_employee.append(task_id)
                               # email when new purchase quotation created
                   if single_employee:
                       ctx = {}
                       if user_email:
                           print("==========single_employeee======",single_employee)
                           ctx['email_from'] = self.env.user.email
                           ctx['user_email'] = user_email
                           ctx['single_employee'] = single_employee
                           # ctx['name'] = single_employee[0].user_id.employee_ids.name
                           ctx['name'] = 'faizan'
                           ctx['lang'] = self.env.user.lang
                           template = self.env.ref('de_project_task_overdue.overdue_mail_template_1')
                           base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                           db = self.env.cr.dbname
                           template.with_context(ctx).sudo().send_mail(self.id, force_send=True, raise_exception=False)
           print("=======list is =====",list)
        # raise UserError(("error"))
