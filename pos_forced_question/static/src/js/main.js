/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_forced_question.pos_forced_question', function(require) {
	"use strict";
	var models = require('point_of_sale.models');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var core = require('web.core');
	var _t = core._t;
	var screens = require('point_of_sale.screens');
	var popup_widget = require('point_of_sale.popups');
	var SuperOrder = models.Order;
	var SuperOrderline = models.Orderline;
	var SuperOrderWidget = screens.OrderWidget;
	var QWeb = core.qweb;

	models.load_models([{
		model:'forced.question.group',
		field: [],
		domain:[],
		loaded: function(self,result) {
			self.db.question_group_by_id = {};
			result.forEach(element => {
				self.db.question_group_by_id[element.id] = element;
			});
		}

	},
	{
		model:'pos.forced.question',
		field: [],
		domain:[],
		loaded: function(self,result) {
			self.db.question_by_id = {};
			result.forEach(element => {
				self.db.question_by_id[element.id] = element;
			});
		}
	}]);
	models.load_fields('product.product','question_group_ids');
	
	var ForcedQuestionPopup = popup_widget.extend({
		template: 'ForcedQuestionPopup',
		events:{
			'click .cancel_question': 'click_cancel',
			'click .tab-link': 'wk_change_tab',
			'click .add_question':'wk_add_question',
		},
		wk_add_question:function(event){
			var self = this;
			var question_id = parseInt($(event.target).data('id'));
			var all_checked_question = self.$('.wk_checked_question:checked');
			var question_list = [];
			all_checked_question.each(function(idx,element){
				question_list.push($(element).data('id'))
			})
			self.options.line.wk_question_ids = question_list;
			self.pos.gui.close_popup();

		},
		wk_change_tab:function(event){
			var content_div_id = $(event.target).data('id');
			if(content_div_id){
				this.$('.tab-content').removeClass('current');
				this.$('.tab-link').removeClass('current');
				$(event.currentTarget).addClass('current');
				this.$(content_div_id).addClass('current');
			}
		},

		click_cancel:function(){
			this.pos.gui.close_popup();
		},
		
		show: function(options){
			var self=this;
			self.options = options || {};
			if (options.product)
				options.image_url = self.wk_get_product_image_url(options.product);
			this._super(self.options);
		},
		wk_get_product_image_url: function(product){
			return window.location.origin + '/web/image?model=product.product&field=image_128&id='+product.id;
		},
	});
	gui.define_popup({ name: 'forced_question', widget: ForcedQuestionPopup });

	models.Order = models.Order.extend({
		add_product: function(product, options){
			var self = this;
			var last_orderline = self.get_last_orderline();
			SuperOrder.prototype.add_product.call(self,product, options);
			var updated_last_orderline = self.get_last_orderline();
			if (product.question_group_ids  && product.question_group_ids.length && !(last_orderline && last_orderline.cid == updated_last_orderline.cid))
				self.pos.gui.show_popup('forced_question',{
					groups:product.question_group_ids,
					product:product,
					line:updated_last_orderline,
				});
		}
	});
	models.Orderline = models.Orderline.extend({
		initialize: function(attr,options){
			var self = this;
			self.wk_question_ids = [];
			self.forced_questions = '';
			SuperOrderline.prototype.initialize.call(self,attr,options);			
		},
		export_for_printing: function(){
			var dict = SuperOrderline.prototype.export_for_printing.call(this);
			dict.wk_question_ids = this.wk_question_ids;
			return dict;
		},
		get_orderline_questions: function(){
			var self = this;
			var question_text = '';
			if(self.wk_question_ids){
				self.wk_question_ids.forEach(function(question_id){
					question_text = question_text + self.pos.db.question_by_id[question_id].name + '\n';
				})
			}	
			return question_text;
		},
		export_as_JSON: function() {
			var self = this;
			var loaded=SuperOrderline.prototype.export_as_JSON.call(this);
			loaded.forced_questions=self.get_orderline_questions();
			loaded.wk_question_ids = self.wk_question_ids;
			return loaded;
		},
		init_from_JSON: function(json) {
			SuperOrderline.prototype.init_from_JSON.call(this,json);
			if(json && json.wk_question_ids){
				this.wk_question_ids = json.wk_question_ids;
			}
		}
		
	});
	screens.OrderWidget.include({
		click_line: function(orderline, event) {
			var self = this;
			self._super(orderline, event)
			if($(event.target).attr('class') == "fa fa-info-circle wkorderline"){
				self.pos.gui.show_popup('forced_question',{
					groups:orderline.product.question_group_ids,
					product:orderline.product,
					line:orderline,
				});
			}
		},
	});

	return ForcedQuestionPopup;
});
