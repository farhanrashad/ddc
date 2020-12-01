/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_order_customization.pos_order_customization', function(require) {
	"use strict";
	var forced_question = require('pos_forced_question.pos_forced_question');
	var screens = require('point_of_sale.screens')
	var models = require('point_of_sale.models')
	var SuperOrderLine = models.Orderline.prototype
	
	forced_question.include({
		wk_add_question:function(event){
			var self = this;
			var available_question_ids = self.options.line.wk_question_ids;
			self._super(event);
			var line = self.options.line;
			var line_price = self.options.line.price;
			var question_ids = self.options.line.wk_question_ids;
			if(available_question_ids.length){
				available_question_ids.forEach(element => {
					line_price = line_price - self.pos.db.question_by_id[element].wk_extra_price
				});
			}
			line.set_unit_price(line_price);
		},
	});

	models.Orderline = models.Orderline.extend({
		set_unit_price: function(price){
			var self = this;
			var question_ids = self.wk_question_ids;
			if(question_ids && question_ids.length){
				question_ids.forEach(element => {
					price = price + self.pos.db.question_by_id[element].wk_extra_price;
				});
			}
			SuperOrderLine.set_unit_price.call(self,price)
		},
	});
	
	screens.OrderWidget.include({
        set_value: function(val) {
            var self = this;
			var order = this.pos.get_order();
			var order_line = order.get_selected_orderline()
            if (order_line) {
                var mode = this.numpad_state.get('mode');
                if( mode === 'price' && val){
                    order_line.wk_question_ids = [];
                }
            }
            self._super(val);
        }
    });
	
});
