# -*- coding: utf-8 -*-
{
    'name': "Sale Order Status",

    'summary': """
        Sale Order Status
        """,

    'description': """
        Sale Order Status
        1-Adding Selection field in sale order model
        2- In-process
        3-  shipped
        4-  pending
        5-  cancelled
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/sale_order_status.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
