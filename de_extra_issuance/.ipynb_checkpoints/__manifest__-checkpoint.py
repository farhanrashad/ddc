# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Extra Issuance Request",
    "category": 'Sales',
    "summary": 'Extra Issuance Request Summary',
    "description": """
	            This module generates the extra issuance requests depends on sale orders
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.0.0.0',
    "depends": ['sale_management','stock','contacts','hr'],
    "data": [
        'wizard/extra_issuance_wizard.xml',
        'report/extra_issuance_report.xml',
        'report/extra_issuance_template.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/extra_issuance_view.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}