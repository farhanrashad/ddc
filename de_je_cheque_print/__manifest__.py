# -*- coding: utf-8 -*-
{
    'name': "Journal Entry Cheque Print",

    'summary': """
        Journal Entry Cheque Print Summary""",

    'description': """
        This Will Prints Cheque from Journal Entry Form
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    
    'category': 'Accounting',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account_accountant','dev_print_cheque'],

    # always loaded
    'data': [
        'views/cheque_print_view.xml',
        'reports/cheque_print_report.xml',
        'reports/cheque_print_template.xml',
    ],
}
