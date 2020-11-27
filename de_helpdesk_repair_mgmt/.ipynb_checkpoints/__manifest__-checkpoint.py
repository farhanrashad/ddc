# -*- coding: utf-8 -*-
{
    'name': "Repair Management",

    'summary': """
    Product Repair
        """,

    'description': """
        Helpdesk - Product Repair Management
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'After-Sales',
    'version': '13.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','de_helpdesk','project','sale_timesheet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/assign_task_technician_views.xml',
        'views/helpdesk_team_views.xml',
        'views/helpdesk_views.xml',
        'views/project_task_views.xml',
        'views/sale_order_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
