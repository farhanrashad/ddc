# -*- coding: utf-8 -*-
{
    'name': "Warehouse Transfer",

    'summary': """
            Warehouse to Warehouse Transfer
            """,

    'description': """
            Stock Warehouse to Warehouse Transfer
            1-Stock Transfer from source warehouse to Transit Location
            2- Stock Transfer from Transit Location to  Destination Warehouse
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock', 'mail','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/internal_transfer_seq.xml',
        'views/warehouse_transfer_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
