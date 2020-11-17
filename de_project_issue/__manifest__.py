# -*- coding: utf-8 -*-
{
    'name': "Project Issues",

    'summary': """
        Showing and Creating issues in Project""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project Issue',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'portal', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/issue_type_wizard.xml',
        'views/templates.xml',
        'views/portal_issue_template.xml',
        'views/project_issue_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
