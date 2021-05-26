# -*- coding: utf-8 -*-
{
    'name': "Secondary UOM",

    'summary': """
        Secondary Unit of Measurment
        """,

    'description': """
        Secondary Unit of Measurement
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/production_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
