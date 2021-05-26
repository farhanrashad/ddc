# -*- coding: utf-8 -*-

{
    "name": "Daily Progress Report",
    "category": 'MRP',
    "summary": 'Adding a wizard , Report Generation Daily Progress',
    "description": """
            Adding a wizard , Report Generation Daily Progress
    """,
    "sequence": 2,
    "web_icon":"",
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '12.0.0.0',
    "depends": ['base','stock','mrp','maintenance'],
    "data": [
        'wizard/daily_progress_report_wizard_view.xml', 
        'security/ir.model.access.csv',
        'report/de_daily_progress_report.xml',
        'report/de_daily_progress_template.xml',
        'views/daily_progress_report_menu.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}



