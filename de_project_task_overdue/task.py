from odoo import models ,fields
from odoo.exceptions import UserError
import datetime

class ProjectTaskInherit(models.Model):

    _inherit = 'project.project'

    is_notify = fields.Boolean(string="Send notification")
    notify_day = fields.Char(string="Set days")

    def action_send_email(self):
        pass
        #    print("enter in action send email")
        #    list = []
        #    task_ids = self.env['project.task'].search([('project_id','=',self.id)])
        #    emid = self.env['hr.employee'].search([('project_id','=',self.id)])
        #    # for id empid
        #    #     if id == task
        #    for task_id in task_ids:
        #        print("=======task_ids======",task_id)
        #        # if
        #        dead_line_date = task_id.date_deadline
        #        print("=======dead_line_date=====",dead_line_date)
        #        print(type(dead_line_date))
        #        current_date = datetime.date.today()
        #        ultimate_dead_line = dead_line_date+self.notify_day
        #        # if current_date == ultimate_dead_line:
        #        #     list.append(task_id)
        #    print("=======list is =====",list)
        # # raise UserError(("error"))
