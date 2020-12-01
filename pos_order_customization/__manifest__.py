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
  "name"                 :  "POS Order Customization",
  "summary"              :  """This module is used to ask question before adding items to the cart which have options like Small or Large, Vegetarian or Non Vegetarian and Sweet or Salted""",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com",
  "description"          :  """https://webkul.com/blog, POS Order Customization, POS Product Customization, POS Product Additional Options, POS Product Options
                               POS Product Question, POS Product Extra Price, POS Extra Price For Product, POS Extra Pice Options""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_order_customization&custom_url=/pos/auto",
  "depends"              :  ['pos_forced_question'],
  "data"                 :  [
                             'views/pos_forced_question_view.xml',
                             'views/template.xml',
                            ],
  "demo"                 :  ['data/pos_order_customization.xml'],
  "qweb"                 :  ['static/src/xml/pos_order_customization.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  24,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}