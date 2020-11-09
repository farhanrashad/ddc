# -*- coding: utf-8 -*-
{
    'name': "Task Auto Assignment",

    'summary': """
        Automatically assign task to user when change stage.""",

    'description': """
        Task Auto Assignment Odoo apps helps for automatically assign user to task based on stage change.
         User can also set default user and default stage for tasks when create a new project.
    """,

    'author': "Yaseen Malik",
    'website': "http://www.dynexcel.co",

    'category': 'Project Tasks',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stage_ext.xml',
        'views/project_ext.xml',
    ],
}
