# -*- coding: utf-8 -*-
{
    'name': "Order Status",

    'summary': """
        Order Status
         - Delivery Status
         - Invoice Status
        """,

    'description': """
        Delivery Status and Invoice Status of Order
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
