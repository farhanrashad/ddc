# -*- coding: utf-8 -*-
{
    'name': "Product Properties",

    'summary': """
    Product Propertise
        """,

    'description': """
        Add Product Propertise
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.3',
    # any module necessary for this one to work correctly
    'depends': ['sale','base','product','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',


    ],
   
}
