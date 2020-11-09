# -*- coding: utf-8 -*-
{
    'name': "Project Task SubTask Checklist",

    'summary': """
        With the help of this module you can divide task or sub task into list of activities.""",

    'description': """
        With the help of this module you can divide task or sub task into list of activities.
        So task and subtask progress will easily control in Odoo project management.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Project Task',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'pad_project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_ext.xml',
        'views/task_checklist.xml',
        'views/project_task_ext.xml',
    ],
}
