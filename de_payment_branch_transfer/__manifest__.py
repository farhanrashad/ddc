# -*- coding: utf-8 -*-
{
    'name': "Payment Branch Transfer",

    'summary': """
        Multi-Branch Amount Transfer""",

    'description': """
        Payment Branch Transfer App offers the feature of transactions between different branches.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_ext.xml',
        'views/payment_transaction.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
