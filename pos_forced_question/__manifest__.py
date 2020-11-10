# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Forced Questions",
  "summary"              :  """This module is used to ask question before adding items to the cart which have options like Small or Large, Vegetarian or Non Vegetarian and Sweet or Salted""",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Forced-Questions.html",
  "description"          :  """https://webkul.com/blog/odoo-pos-forced-questions/, POS Forced Questions, Frequent Questions for Product, Product options, Product Questions""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_forced_question&custom_url=/pos/web",
  "depends"              :  [
                             'point_of_sale',
                             'product',
                            ],
  "data"                 :  [
                             'views/pos_forced_question_view.xml',
                             'views/template.xml',
                             'views/question_sequence.xml',
                             'security/ir.model.access.csv',
                            ],
  "demo"                 :  ['data/pos_force_question_demo.xml'],
  "qweb"                 :  ['static/src/xml/pos_forced_question.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  45,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}