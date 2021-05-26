# -*- coding: utf-8 -*-
{
    'name': "Job Order",

    'summary': """
        Calculate material
        """,

    'description': """
        Job Order to Calculate Material Quantities on the basis of formula
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '3.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','sale','stock','purchase','sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/bom_views.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/mrp_views.xml',
        'views/purchase_views.xml',
        'views/job_rule_views.xml',
        'views/job_order_views.xml',
        'views/job_order_report.xml',
		'views/sale_views.xml',
		'views/picking_views.xml',
        'views/weaving_contract_report.xml',
        'views/stock_move_views.xml',
        'views/product_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}