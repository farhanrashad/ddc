# -*- coding: utf-8 -*-
{
    'name': "Production Order Cost",

    'summary': """
        Production Order Cost 
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','stock','product'],

    # always loaded
    'data': [
        'report/direct_cost_report.xml',
        'report/direct_cost_report_template.xml',
        'security/ir.model.access.csv',
        'views/direct_cost_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
