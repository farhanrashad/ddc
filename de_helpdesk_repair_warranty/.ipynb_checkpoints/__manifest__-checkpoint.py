# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Repair Warranty",

    'summary': """
        Helpdesk Repair Warranty
        """,

    'description': """
        This module is used to link warranty in repair
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','repair','de_sale_warranty'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/repair_views.xml',
        'views/sales_warranty_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
