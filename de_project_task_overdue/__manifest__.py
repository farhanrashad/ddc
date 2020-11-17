# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name":  "Project Task Overdue",
  "summary":  "Module for project task overdue",
  "category":  "Extra tools",
    "description": """
	 
   
    """,
    "sequence": 3,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.1.0.0',
    "depends": ['project'],
    "data": [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        # 'views/student_data_view.xml',
        'views/task.xml',
#         'report/employee_report_pdf.xml',
    ],
    
    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
