# -*- coding: utf-8 -*-
{
    'name': "Global Reference",

    'summary': """
    Global Order Reference
        """,

    'description': """
        This reference will use on all printing docuemnts. 
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','mrp','stock','de_job_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/job_order_views.xml',
        'views/mrp_views.xml',
        'views/purchase_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
