# -*- coding: utf-8 -*-
{
    'name': "Partner Balance",

    'summary': """
        Partner balance.""",

    'description': """
        Partner balance.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    'category': 'accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_ext.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
