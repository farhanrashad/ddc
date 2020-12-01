# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Repair Warranty",

    'summary': """
    Add warranty in helpdesk
        """,

    'description': """
        Add Warranty in Helpdesk
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['de_helpdesk_site','de_sale_warranty'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        
        'views/sale_warranty_views.xml',
        'views/project_task_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/account_invoice_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
