# -*- coding: utf-8 -*-
{
    'name': "Customer Balance",

    'summary': """
    Customer Balance
        """,

    'description': """
        Customer Balance
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','point_of_sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/partner_views.xml',
        'views/pos_views.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
