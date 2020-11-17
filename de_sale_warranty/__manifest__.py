# -*- coding: utf-8 -*-
{
    'name': "Sales Warranty",

    'summary': """
    Sale Product Warranty
        """,

    'description': """
        Product warranty to customers on sales
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','sales_team','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'data/warranty_sequence.xml',
        'views/sales_warranty_views.xml',
        'views/product_views.xml',
        'views/warranty_card_report.xml',
        'views/sales_warranty_templates.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'wizard/warranty_claim.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
