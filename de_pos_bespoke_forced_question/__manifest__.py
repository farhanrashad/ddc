# -*- coding: utf-8 -*-
{
    'name': "POS Bespoke Order",

    'summary': """
    Bespoke Order from POS Order with Question
        """,

    'description': """
        Bespoke Order from POS Order with Question
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','pos_forced_question','stock','mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/bespoke_seq.xml',
        'views/product_views.xml',
        'views/pos_order_views.xml',
        'views/bespoke_order_views.xml',
        'views/pos_order_line_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
