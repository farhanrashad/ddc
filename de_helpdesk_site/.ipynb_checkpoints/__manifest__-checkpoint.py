# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Site",

    'summary': """
        Helpdesk Service Site Details
        """,

    'description': """
        Service site detail of customer
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'After-Sales',
    'version': '13.0.0.5',

    # any module necessary for this one to work correctly
    'depends': ['base','de_helpdesk','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/helpdesk_site_views.xml',
        'views/helpdesk_templates.xml',
        'views/helpdesk_project_site_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
