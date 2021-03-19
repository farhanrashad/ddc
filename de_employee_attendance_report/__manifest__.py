# -*- coding: utf-8 -*-
{
    'name': "Employee Attendance Report",
    
    'version': '13.0.0.0',
    'category': 'Employee',
    'summary': 'Employee Attendance Report',
    'sequence': 3,
    'description': """  """,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",
#     'license': 'LGPL-3',
    'depends': ['base','hr_attendance','report_xlsx'],
    
    'data': [
        'security/ir.model.access.csv',
        'wizards/employee_attendance.xml',
        'views/employee_checkin_checkout.xml',
        'views/employee_attendance_menu.xml',
        'report/employee_att_report.xml',
        'report/employee_att_template.xml',
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}