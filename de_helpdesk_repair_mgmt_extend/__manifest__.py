# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Repair Extend",

    'summary': """
            Helpdesk Repair Extend
        """,

    'description': """
        Helpdesk Repair Extend
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",


    'category': 'Helpdesk',
    'version': '13.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','de_helpdesk','de_helpdesk_repair_custom_views'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
