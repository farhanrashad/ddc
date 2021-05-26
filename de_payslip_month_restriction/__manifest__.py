# -*- coding: utf-8 -*-
{
    'name' : 'Payslip Restriction For Month',
    'version': '13.0.0.0',
    'author' : 'Dynexcel',
    'website' : 'http://www.dynexcel.co',
    'category' : 'payroll',
    'summary': 'This module will restrict user to generate multiple payslips for an employee.',
    'description': """

This module will restrict user to generate multiple payslips for an employee

            """,
    'depends':['hr', 'hr_payroll'],
    'data' : ['views/payslip_view.xml'],
    'installable':True,
    'auto_install':False
}

