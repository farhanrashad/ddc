# -*- coding: utf-8 -*-
{
    'name': "Job Order Enhancement",

    'summary': """
        Job Order Enhancement 
        Get All Component of BOM in Material Planning
        """,

    'description': """
        Job Order Enhancement 
        1- Get component of BOM in hierarchical manner
        2- All component of BOM store in Material Planning Tab
        3- Component Having type Subcontracting  Purchase Order created and 
        Component having type Manufacturing  Production Order Created
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_job_order','de_product_weight','stock','purchase','mrp','sale','account_reports','account','product'],

    # always loaded
    'data': [
        'data/server_action.xml',
        'security/ir.model.access.csv',
        'views/job_order.xml',
        'views/mrp_production.xml',
        'views/stock_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
