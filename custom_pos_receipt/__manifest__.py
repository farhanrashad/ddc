# -*- coding: utf-8 -*-
{
    'name': 'POS Custom Receipt',
    'version': '1.0',
    'category': 'Point Of Sale',
    'summary': 'Customized Receipt of Point Of Sales',
    'website': 'www.dynexcel.co',
    'author': 'Dynexcel',
    'images': ['static/description/banner.jpg'],
    'description': "Customized our point of sale receipt",
    'depends': ['base', 'point_of_sale'],
    "data": [
        'views/templates.xml',
        'views/pos_config.xml',
    ],
    'demo': [],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
}
