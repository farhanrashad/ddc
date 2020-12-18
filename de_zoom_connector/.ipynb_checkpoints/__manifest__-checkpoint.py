# -*- coding: utf-8 -*-
#################################################################################
# Author      : Dynexcel (<www.dynexcel.com>)
# Copyright(c): 2015-Present Dynexcel.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': '[5% OFF] Zoom Meetings Integration',
    'version': '13.0.0.2',
    'summary': 'Create and share Zoom video meetings through odoo calendar.',
    'description': """
        Create and share Zoom video meetings through odoo calendar.
    """,
    'category': 'Extra Tools',
    'website': 'http://www.dynexcel.com',
    'author': 'Dynexcel',
    'price': 95.00,
    'currency': 'USD',
    'images': ['static/description/banner.gif'],
    'depends': ['calendar', 'mail'],
    'data': [
            'security/ir.model.access.csv',
            'data/external_user_mail_data.xml',
            'data/mail_data.xml',
            'view/user_views.xml',
            'view/calendar_views.xml',
            'view/company_views.xml',
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
