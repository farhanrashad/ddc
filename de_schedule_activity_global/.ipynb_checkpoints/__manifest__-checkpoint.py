# -*- coding: utf-8 -*-
{
    'name': "Activities Management",

    'summary': """
        Schedule Activities""",

    'description': """
        Schedule Activities
    """,
    'author': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'price': 49,
    'currency': 'USD',
    'company': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'website': "http://www.dynexcel.com",
    'category': 'Discuss',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/schedule_activities_view.xml',
        'views/activity_menuitems.xml',
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/banner.jpg'],

}
