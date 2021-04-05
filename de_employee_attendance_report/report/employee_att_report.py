import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import datetime
from odoo import api, fields, models, _
from datetime import date, timedelta



class AttendanceReport(models.AbstractModel):
    _name = 'report.de_employee_attendance_report.employee_template'
    
    def get_attendance(self, employee_id, date):
        sql1 = """
                select check_in, check_out, worked_hours from hr_attendance
                where employee_id = """ + str(employee_id) + """ and date(check_in) = '""" + str(date) + """' 
                order by check_in asc
                LIMIT 2
                """
        self.env.cr.execute(sql1)
        result = self.env.cr.fetchall()

        if result:
            count_hours = 0
            record_list = [None, None, None, None, None]
            list_index = 0

            for rec in result:
                count_hours = count_hours + rec[2]

                for r in rec:
                    if type(r) != float:
                        record_list[list_index] = r
                        list_index = list_index + 1

            work_hour = round(count_hours, 2)
            record_list[4] = work_hour

            return [tuple(record_list)]
        else:
            record_list = [(None, None, None, None, None)]
            return record_list


    def _get_report_values(self, docids, data=None):
        emp_list = []
        date_list = []

        all_emp = self.env['hr.employee'].search([])
        for emp in all_emp:
            emp_list.append(emp.id)

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']

        f_dt = datetime.strptime(date_from, "%Y-%m-%d")
        f_dt = f_dt.date()
        t_dt = datetime.strptime(date_to, "%Y-%m-%d")
        t_dt = t_dt.date()

        delta = t_dt - f_dt
        for i in range(delta.days + 1):
            day = f_dt + timedelta(days=i)
            date_list.append(str(day))
            i = i + 1

        return {
            'doc_ids': self.ids,
            'doc_model': 'hr_attendance.hr.attendance',
            'get_attendance': self.get_attendance,
            'date_list': date_list,
            'all_employees': emp_list,
            'employee_ids': data['form']['employee'],
            'date_from': data['form']['date_from'],
            'date_to': data['form']['date_to'],
        }