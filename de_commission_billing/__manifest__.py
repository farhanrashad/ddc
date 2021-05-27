# -*- coding: utf-8 -*-

{
    'name': 'Commission Billing ',
    'category': '',
    'summary': 'adding new fields in res.partner model',
    'description': """
            This module is about to add new fields in res.partner model.
                    """,
    'depends': ['base','purchase','contacts'],
    'data': [
        'views/commission_billing_views.xml',
    ],
    # 'qweb': ['views/project_task_view.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
