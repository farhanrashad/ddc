# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Payment Statement",
    "category": 'Invoicing',
    "summary": 'Payment Bank Statement',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.1.0.0',
    "depends": ['account'],
    "data": [
        'security/ir.model.access.csv',
        'views/payment_statement_view.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
