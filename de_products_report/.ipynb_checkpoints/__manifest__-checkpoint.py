# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Product Report",
    "category": 'Sales',
    "summary": 'Product Reports By Dynexcel',
    "description": """
	 This module is generating the pdf reports of the products.
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '11.0.0.0',
    "depends": ['sale','product'],
    "data": [
        'reports/product_report.xml',
        'reports/product_report_template.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}