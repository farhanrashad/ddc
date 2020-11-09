# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Repair",

    'summary': """
        Project, Tasks, Repair""",

    'description': """
        Repair Products from helpdesk tickets
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'After-Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','de_helpdesk','repair'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/repair_views.xml',
        'views/helpdesk_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}