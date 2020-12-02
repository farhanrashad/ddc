# -*- coding: utf-8 -*-

{
    'name': 'Measurement Note In POS',
    'summary': """add measurement note in order line from the pos interface. """,
    'version': '12.0.1.0.1',
    'description': """The module enables to add multiple order line from the pos interface and other than
    selection of the order note text is also enabled""",
    'author': 'Dynexcel',
    'company': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'category': 'Point of Sale',
    'depends': ['base', 'point_of_sale'],
    'license': 'AGPL-3',
    'data': [
        'views/pos_templates.xml',
        'views/pos_order_views.xml',
        'views/pos_config_views.xml',
        'security/ir.model.access.csv',
        'views/pos_order_notes_views.xml',
    ],
    'qweb': [
        'static/src/xml/notes.xml',
        'static/src/xml/pos_receipt.xml',
            ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,

}