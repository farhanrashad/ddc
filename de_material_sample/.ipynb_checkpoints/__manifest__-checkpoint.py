# -*- coding: utf-8 -*-
#################################################################################
# Author      : Dynexcel (<https://dynexcel.com/>)
# Copyright(c): 2015-Present dynexcel.com
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
{
  "name"                 :  "Garment Costing",
  "summary"              :  "Garment Design Sample Costing",
  "category"             :  "Custom",
  "version"              :  "1.2",
  "sequence"             :  1,
  "author"               :  "Dynexcel",
  "license"              :  "AGPL-3",
  "website"              :  "http://dynexcel.com",
  "description"          :  """

""",
  "live_test_url"        :  "",
  "depends"              :  [
                             'base','portal'
                            ],
  "data"                 :  [
      'report/sample_report.xml',
      'report/sample_report_templates.xml',
      'security/ir.model.access.csv',
      'views/sample_design_form_view.xml',
                            ],
  "images"               :  [''],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  0,
  "currency"             :  "EUR",
  "images"		 :[''],
}