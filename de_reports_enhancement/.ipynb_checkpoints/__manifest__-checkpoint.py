# -*- coding: utf-8 -*-
{
    'name': "Print Reports",

    'summary': """
    Print Reports Enhacement
        """,

    'description': """
        Add fields in print reports
        1. Sale Order
        2. Performa Invoice
        3. Invoice
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','purchase','mrp','de_product_weight','de_job_order','de_sale_global_ref','de_picking_gatepass','de_secondary_uom_qty'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_report_template.xml',
        'views/purchase_order_report_template.xml',
        'views/delivery_slip_report_template.xml',
        'views/mo_report_template.xml',
        'views/gatepass_report_template.xml',
        'views/invoice_report_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}