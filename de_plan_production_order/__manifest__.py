# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Production Plan Order",
    "category": 'Production Plans',
    "summary": 'Production Plan Order',
    "description": """
            This module will plan production orders
    """,
    "sequence": 2,
    "web_icon":"static/src/images/icon.png",
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.1.0.0',
    "depends": ['mrp'],
    "data": [
        'security/ir.model.access.csv',
        'security/production_plan_order.xml',
        'data/productionPlan.xml',
        'report/production_plan_order_report.xml',
        'report/production_plan_order_report_pdf.xml',
        'views/production_plan_order_view.xml',
        'views/production_plan_order_menu.xml',

        # 'wizards/student_wizard.xml'


    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}



