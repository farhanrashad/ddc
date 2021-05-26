# -*- coding: utf-8 -*-
{
    'name': "Inventory Gatepass",

    'summary': """
        Inventory Gatepass
        """,

    'description': """
        Inventory Gatepass
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'report/gatepass_template.xml',
        'report/gatepass_report.xml',
        
        'security/ir.model.access.csv',
        'data/gp_sequence.xml',
        'views/stock_move_line_views.xml',
        'views/gatepass_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
