# -*- coding: utf-8 -*-
{
    'name': '[5% OFF] Zoom Integration',
    'version': '13.0.1',
    'summary': 'Create and share Zoom video conferences with other users and external partners',
    'author': 'Dynexcel',
    'sequence': 2,
    'description': """
        Zoom provides videotelephony and is used for teleconferencing, telecommuting, distance education, and social relations.
    """,
    'category': 'Extra Tools',

    'website': 'www.Dynexcel.com',
    'images': ['static/description/banner.gif'],
    "license": "AGPL-3",
    'depends': ['calendar', 'mail'],
    'data': [
            'security/ir.model.access.csv',
            'data/external_user_mail_data.xml',
            'data/mail_data.xml',
            'view/user_email.xml',
            'view/calendar_views.xml',
            'view/company_credetionals.xml',
            'view/calendar_templates.xml',
            'wizard/new_zoom_user.xml',
            'wizard/message_wizard.xml',

    ],
    'external_dependencies': {
        'python': ['zoomus'],
    },

    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
