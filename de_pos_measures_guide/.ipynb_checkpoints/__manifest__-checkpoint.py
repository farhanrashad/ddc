# -*- coding: utf-8 -*-

{
    'name': 'POS Measurement Guide',
    'summary': """The module enables to add measurment guide in pos line """,
    'version': '13.0.1.0.1',
    'description': """The module enables to add measurement guide in POS order line from the pos interface """,
    'author': 'Dynexcel',
    'company': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'category': 'Point of Sale',
    'depends': ['base', 'point_of_sale'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config_views.xml',
        'views/templates.xml',
        'views/measures_guide_views.xml',
        'views/pos_order_views.xml',
    ],
    'qweb': [
        'static/src/xml/pos_measures.xml',
        'static/src/xml/pos_receipt.xml',
            ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,

}