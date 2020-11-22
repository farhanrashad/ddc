# -*- coding: utf-8 -*-
{
    'name': "Reserve Order Extention",

    'summary': """
    Accounting Adjustment
        """,

    'description': """
        Reserve Order Accounting Adjustments
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','pos_reserve_order_app'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_order_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
