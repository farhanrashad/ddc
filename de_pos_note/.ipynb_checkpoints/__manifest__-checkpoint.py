# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Sayooj A O(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Order Note In POS',
    'summary': """The module enables to add Note in order line from the pos interface. """,
    'version': '12.0.1.0.0',
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
        #'security/ir.model.access.csv',
    ],
    'qweb': ['static/src/xml/notes.xml'],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,

}