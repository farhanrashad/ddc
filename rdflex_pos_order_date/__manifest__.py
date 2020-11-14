# -*- coding: utf-8 -*-
{
    'name': "POS Order Date",
    'summary': """
        Add option to select pos order date
    """,
    'description': """
        Add date selector in payment screen so user can choose pos order date
    """,
    'author': "RDFlex",
    'company': 'RDFlex',
    'maintainer': 'RDFlex',
    'website': "https://rdflex.com",
    'category': 'Point of Sale',
    'license': 'OPL-1',
    'version': '1',
    'depends': ['point_of_sale'],
    'images': ['static/description/banner.jpg'],
    'data': [
        'views/pos_order_date_assets.xml',
    ],
    'qweb': ['static/src/xml/pos_order_date.xml'],

}