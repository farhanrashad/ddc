# -*- coding: utf-8 -*-
{
    'name': "Helpdesk SLA",

    'summary': """
    Service Level Agreement
        """,

    'description': """
        Helpdesk (Service Level Agreement)
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    'category': 'After-Sales',
    'version': '0.2',

    'depends': ['base','de_helpdesk'],

    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_sla_views.xml',
        'views/helpdesk_ticket_type_views.xml',
        'views/helpdesk_ticket_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
