# -*- coding: utf-8 -*-
{
    'name': "Invoicing Category",

    'summary': """
     Tags field added in Invoicing    
     """,

    'description': """
    Tags Field added in Invoicing in following form
       1- Customer--> Invoice
       2- Vendor--> Bill
       3- related to partner_id
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/de_invoicing_customer_invoice.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
