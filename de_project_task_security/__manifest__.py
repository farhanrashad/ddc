# -*- coding: utf-8 -*-
{
    'name': "de_project_task_security",

    'summary': """
        Create a auto security group named = "Task Limited Access" """,

    'description': """
        Create a auto security group named = "Task Limited Access"
        make readonly the following fields for above group "Task Limited Access" means a user assign this task will not 
        able to edit the values of below given fields.
        Assigned to,Deadline,Description,Planned Hours
    """,

    'author': "dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','hr_timesheet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/limited_access_group.xml',
        'views/updated_view_access.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
