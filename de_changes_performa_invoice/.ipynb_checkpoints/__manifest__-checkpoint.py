# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Modification in Peroforma Invoice",
    "category": 'Sale',
    "summary": 'Changes in Peroforma Invoice in sale order and stock',
    "description": """
	 Changes in Peroforma Invoice in sale order and note field in stock
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.0',
    "depends": ['base','sale', 'stock'],
    "data": [
#         'security/ir.model.access.csv',
        'report/performa_invoice_report_inh.xml',
        'report/performa_invoice_report_pdf.xml',
        'views/performa_invoice_view_inh.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
