# -*- coding: utf-8 -*-
{
    'name': "Order Analysis",

    'summary': """
        Order Analysis include - 
        Sale Order
        Purchase Order/Subcontracting Order
        Manufacturig Order
        Movement
        
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '1.8',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','stock','mrp','de_sale_global_ref','de_product_weight','de_job_order','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'report/sale_report_views.xml',
        #'report/order_stock_report_views.xml',
        'report/order_subcontract_views.xml',
        'report/order_production_report_views.xml',
        'report/sale_stock_report_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
