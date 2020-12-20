# -*- coding: utf-8 -*-
{
    'name': "Schedule Activity",

    'summary': """
        Schedule Activity Global""",

    'description': """
        Schedule Activity Global
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Activity',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/schedule_activities_view.xml',
        'views/activity_menuitems.xml',
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
