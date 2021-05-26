# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Section Wise Total",
    "summary": 'Section Wise Total for Sale/Purchase',
    "sequence": 1,

    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.0.0.1',

    "depends": ['base','sale', 'purchase'],
    "data": [
        'security/ir.model.access.csv',
        'views/section_wise_total.xml',
    ],

    "installable": True,
    "application": False,
    "auto_install": False,
}
