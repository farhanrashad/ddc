# -*- coding: utf-8 -*-
{
    'name': "Project Task Revision",

    'summary': """
         Revision Management By Dynexcel""",

    'description': """
        Long description of module's purpose
    """,

    'author': "By Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/project_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode

}
