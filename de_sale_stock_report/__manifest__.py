# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################
{
    'name': 'Sale Stock',
    'version': '0.2',
    'summary': 'This module will add Sale Stock Report',
    'description': 'This module provides the movement of individual products with opening and closing stocks',
    'author': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'company': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'depends': ['base', 'stock'],
    'category': 'Inventory',
    'demo': [],
    'data': ['views/sale_stock_views.xml',
             'security/ir.model.access.csv',
             'report/sale_stock_report.xml',
             'report/sale_stock_report_template.xml'],
    'installable': True,
    'images': ['static/description/banner.png'],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'live_test_url': 'https://youtu.be/5OqXXKO6gRA',
}
