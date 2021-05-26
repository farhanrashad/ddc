# -*- coding: utf-8 -*-
{
    'name': "POS Customization",

    'summary': """
        Modifications in built in modules""",

    'description': """
        This module is for customization purposes.
    """,

    'author': "Yaseen Malik",
    'website': "http://www.dynexcel.co",

    'category': 'Customization',
    'version': '0.1',

    'depends': ['base', 'stock', 'mrp', 'account', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/job_order_tolerance.xml',
        'views/product_ext.xml',
        'views/production_lot_ext.xml',
        'views/job_order.xml',
        'data/job_order_data.xml',
    ],
}