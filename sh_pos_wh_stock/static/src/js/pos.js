odoo.define('sh_pos_wh_stock.screens', function(require) {
    "use strict";
    
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var PopupWidget = require('point_of_sale.popups');
    var rpc = require('web.rpc');
    var ActionManager = require('web.ActionManager');
    var Session = require('web.session');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var DB = require('point_of_sale.DB');
    
    var QWeb = core.qweb;
    var _t = core._t;
    
    models.load_models({
        model: 'stock.quant',
        fields: ['id', 'product_id', 'location_id', 'company_id', 'quantity', 'reserved_quantity'],
        domain: function(self) {
            return [
                ['location_id.usage', 'in', ['internal']],
            ];
        },
        loaded: function(self, qunats) {
            self.db.add_qunats(qunats);
        }
    });
    models.load_models({
        model: 'stock.warehouse',
        fields: ['id', 'lot_stock_id', 'code','name'],
        loaded: function(self, warehouses) {
            self.db.add_warehouse(warehouses);
        }
    });
    models.load_models({
        model: 'stock.location',
        fields: ['id', 'name','display_name','location_id'],
        loaded: function(self, locations) {
            self.db.add_location(locations);
        }
    });
    models.load_models({
        model: 'stock.picking.type',
        fields: ['id', 'name','default_location_src_id'],
        loaded: function(self, picking_types) {
            self.db.add_picking_types(picking_types);
        }
    });
    DB.include({
        init: function(options) {
            this._super(options);
            this.qunats = [];
            this.qunat_by_id = {};
            this.quant_by_product_id = {};
            this.picking_type_by_id = {};
            this.warehouse_by_id = {};
            this.lot_stock_list = [];
            this.location_by_id = {};
        },
        add_picking_types: function(picking_types){
        	for (var i = 0, len = picking_types.length; i < len; i++) {
       		 	var picking_type = picking_types[i];
	       		this.picking_type_by_id[picking_type['id']] = picking_type
	       	}
        },
        add_qunats: function(qunats) {
            if (!qunats instanceof Array) {
            	qunats = [qunats];
            }
            for (var i = 0, len = qunats.length; i < len; i++) {
                var qunat = qunats[i];
                this.qunats.push(qunat);
                this.qunat_by_id[qunat.id] = qunat;
                if(qunat.product_id[0] in this.quant_by_product_id){
                	
                	var tmp_loc_dic = this.quant_by_product_id[qunat.product_id[0]]
                	if(qunat.location_id[0] in tmp_loc_dic){
                		
                		var tmp_qty = tmp_loc_dic[qunat.location_id[0]]
                		tmp_loc_dic[qunat.location_id[0]] = qunat.quantity + tmp_qty
                		
                	}else{
                		tmp_loc_dic[qunat.location_id[0]] = qunat.quantity
                	}
                	this.quant_by_product_id[qunat.product_id[0]] = tmp_loc_dic
                	
                }else{
                	var location_qty_dic = {};
                	location_qty_dic[qunat.location_id[0]] = qunat.quantity
                	this.quant_by_product_id[qunat.product_id[0]] = location_qty_dic;
                }
                
            }
        },
        add_warehouse: function(warehouses) {
        	for (var i = 0, len = warehouses.length; i < len; i++) {
        		 var warehouse = warehouses[i];
        		this.warehouse_by_id[warehouse.lot_stock_id[0]] = warehouse
        		this.lot_stock_list.push(warehouse.lot_stock_id[0])
        	}
        },
        add_location: function(locations) {
        	for (var i = 0, len = locations.length; i < len; i++) {
	       		 var location = locations[i];
	       		this.location_by_id[location['id']] = location
	       	}
       },
    });
    screens.PaymentScreenWidget.include({
    	validate_order: function(force_validation) {
    		var self = this;
            if (this.order_is_valid(force_validation)) {
                var pos_order = this.pos.get_order();
                self.finalize_validation();
                // modify stock dic
                if (this.pos.config.picking_type_id) {
                    var picking_type = this.pos.db.picking_type_by_id[this.pos.config.picking_type_id[0]];
                    if (picking_type && picking_type.default_location_src_id) {
                        var location_id = picking_type.default_location_src_id[0];
                        var order = this.pos.get_order();
                        if (location_id) {
                            var quant_by_product_id = this.pos.db.quant_by_product_id;
                            $.each(quant_by_product_id, function (product, value) {
                                for (var i = 0; i < order.orderlines.models.length; i++) {
                                    if (order.orderlines.models[i].product.id && order.orderlines.models[i].product.id == product) {
                                        $.each(value, function (location, qty) {
                                            if (location == location_id) {
                                                value[location] = qty - order.orderlines.models[i].quantity;
                                            }
                                        });
                                    }
                                }
                            });
                        }
                    }
                }
            }
        },
    });
    
        
    var ProductQtyPopup = PopupWidget.extend({
        template: 'ProductQtyPopup',
        init: function(parent, args) {
            this._super(parent, args);
           
        },
        show: function(options){
            options = options || {};
	          var self = this;
	          this._super(options);
	          this.title = options['title'];
	          var product_id = options['product_id'];
	          var quant_by_product_id = this.pos.db.quant_by_product_id[product_id]
	          this.renderElement();
	          var table_html = '<tr><th width="70%" class="head_td">Location</th><th width="30%" class="head_td">Quantity</th></tr>'
	          var total_qty = 0;
	          if(quant_by_product_id){
	        	  $.each( quant_by_product_id, function( key, value ) {
		        	  
		        	  var location = self.pos.db.location_by_id[key]
		        	  if(value > 0 || value < 0){
		        		  if(self.pos.db.lot_stock_list.includes(location['id'])){
			        		  table_html += '<tr><td class="data_td">'+location['display_name']+'</td><td class="data_td">'+value+'</td></tr>'
			        		  total_qty += parseInt(value)
		        		  }
		        		  else if(location['location_id'] && self.pos.db.lot_stock_list.includes(location['location_id'][0])){
		        			  table_html += '<tr><td class="data_td">'+location['display_name']+'</td><td class="data_td">'+value+'</td></tr>'
		        			  total_qty += parseInt(value)
		        		  }
		        		  
		        	  }
		        	 
	         
	        	  });
	          }
	          
	          table_html += '<tr><th width="70%" class="footer_td">Total</th><th width="30%"  class="footer_td">'+total_qty+'</th></tr>'
	          $('.wh_qty').html(table_html)
	          
	          this.$('.button.confirm').click(function() {
	              self.gui.close_popup();
	          });

        }
    });
    gui.define_popup({name:'product_qty_popup', widget: ProductQtyPopup});
    
    screens.ProductListWidget.include({
       
    	on_click_show_qty: function (e) {
	        var self = this;
	        e.stopPropagation();
	        var $target = $(e.currentTarget).parent();
	        var product_id = $target.data('product-id');
	        var product = this.pos.db.get_product_by_id(product_id);
	        self.gui.show_popup('product_qty_popup',{'title': 'Product Stock','product_id':product_id});
	    },
    	 renderElement: function() {
    	        var el_str  = QWeb.render(this.template, {widget: this});
    	        var el_node = document.createElement('div');
    	            el_node.innerHTML = el_str;
    	            el_node = el_node.childNodes[1];

    	        if(this.el && this.el.parentNode){
    	            this.el.parentNode.replaceChild(el_node,this.el);
    	        }
    	        this.el = el_node;
    	        var list_container = el_node.querySelector('.product-list');
    	        for(var i = 0, len = this.product_list.length; i < len; i++){
    	            var product_node = this.render_product(this.product_list[i]);
    	            
    	            product_node.addEventListener('click',this.click_product_handler);
    	            product_node.addEventListener('keypress',this.keypress_product_handler);
    	            
    	            if (this.pos.config.sh_display_stock) {
	                	 product_node.querySelector('.product-image-icon').addEventListener('click',this.on_click_show_qty);
	                 }
    	            	
    	            list_container.appendChild(product_node);
    	        }
    	    },
    });
    screens.OrderWidget.include({

	    on_click_show_qty: function(orderline){
	    	var self = this;
	        this.pos.get_order().select_orderline(orderline);
	        var line = this.pos.get_order().get_selected_orderline();
	        if (line) {
    			var product = line.get_product();
    	        self.gui.show_popup('product_qty_popup',{'title': 'Product Stock','product_id':product['id']});
	        }
	    },
 	   render_orderline: function(orderline){
 	        var el_str  = QWeb.render('Orderline',{widget:this, line:orderline}); 
 	        var el_node = document.createElement('div');
 	            el_node.innerHTML = _.str.trim(el_str);
 	            el_node = el_node.childNodes[0];
 	            el_node.orderline = orderline;
 	            el_node.addEventListener('click',this.line_click_handler);
 	        var el_lot_icon = el_node.querySelector('.line-lot-icon');
 	        if(el_lot_icon){
 	            el_lot_icon.addEventListener('click', (function() {
 	                this.show_product_lot(orderline);
 	            }.bind(this)));
 	        }
 	     
 	      var el_image_icon = el_node.querySelector('.product-image-icon');
 	        if(el_image_icon){
 	        	el_image_icon.addEventListener('click', (function() {
 	                this.on_click_show_qty(orderline);
 	            }.bind(this)));
 	        }
 	        
 	        orderline.node = el_node;
 	        return el_node;
 	    },
    	
    });
    
    
});
