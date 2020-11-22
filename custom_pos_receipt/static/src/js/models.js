/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('custom_pos_receipt.custom_pos_receipt', function(require) {
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

	exports.PosModel = Backbone.Model.extend({
	    initialize: function(session, attributes) {
        Backbone.Model.prototype.initialize.call(this, attributes);
        var  self = this;
        this.flush_mutex = new Mutex();                   // used to make sure the orders are sent to the server once at time
        this.chrome = attributes.chrome;
        this.gui    = attributes.gui;

        this.proxy = new devices.ProxyDevice(this);              // used to communicate to the hardware devices via a local proxy
        this.barcode_reader = new devices.BarcodeReader({'pos': this, proxy:this.proxy});

        this.proxy_queue = new devices.JobQueue();           // used to prevent parallels communications to the proxy
        this.db = new PosDB();                       // a local database used to search trough products and categories & store pending orders
        this.debug = core.debug; //debug mode

        // Business data; loaded from the server at launch
        this.company_logo = null;
        this.company_logo_base64 = '';
        this.currency = null;
        this.shop = null;
        this.company = null;
        this.user = null;
        this.users = [];
        this.partners = [];
        this.cashregisters = [];
        this.taxes = [];
        this.pos_session = null;
        this.config = null;
        this.units = [];
        this.units_by_id = {};
        this.default_pricelist = null;
        this.order_sequence = 1;
        this.is_partner_pos = null;
        window.posmodel = this;

        // these dynamic attributes can be watched for change by other models or widgets
        this.set({
            'synch':            { state:'connected', pending:0 },
            'orders':           new OrderCollection(),
            'selectedOrder':    null,
            'selectedClient':   null,
            'cashier':          null,
        });

        this.get('orders').bind('remove', function(order,_unused_,options){
            self.on_removed_order(order,options.index,options.reason);
        });

        // Forward the 'client' attribute on the selected order to 'selectedClient'
        function update_client() {
            var order = self.get_order();
            this.set('selectedClient', order ? order.get_client() : null );
        }
        this.get('orders').bind('add remove change', update_client, this);
        this.bind('change:selectedOrder', update_client, this);

        // We fetch the backend data on the server asynchronously. this is done only when the pos user interface is launched,
        // Any change on this data made on the server is thus not reflected on the point of sale until it is relaunched.
        // when all the data has loaded, we compute some stuff, and declare the Pos ready to be used.
        this.ready = this.load_server_data().then(function(){
            return self.after_load_server_data();
        });
    },
    after_load_server_data: function(){
        this.load_orders();
        this.set_start_order();
        if(this.config.use_proxy){
            if (this.config.iface_customer_facing_display) {
                this.on('change:selectedOrder', this.send_current_order_to_customer_facing_display, this);
            }

            return this.connect_to_proxy();
        }
    },
    destroy: function(){
        // FIXME, should wait for flushing, return a deferred to indicate successfull destruction
        // this.flush();
        this.proxy.close();
        this.barcode_reader.disconnect();
        this.barcode_reader.disconnect_from_proxy();
    },
    connect_to_proxy: function(){
        var self = this;
        var  done = new $.Deferred();
        this.barcode_reader.disconnect_from_proxy();
        this.chrome.loading_message(_t('Connecting to the PosBox'),0);
        this.chrome.loading_skip(function(){
                self.proxy.stop_searching();
            });
        this.proxy.autoconnect({
                force_ip: self.config.proxy_ip || undefined,
                progress: function(prog){
                    self.chrome.loading_progress(prog);
                },
            }).then(function(){
                if(self.config.iface_scan_via_proxy){
                    self.barcode_reader.connect_to_proxy();
                }
            }).always(function(){
                done.resolve();
            });
        return done;
    },
    models: [
        {
            label:  'version',
            loaded: function(self){
                return session.rpc('/web/webclient/version_info',{}).done(function(version) {
                    self.version = version;
                });
            },
        },
        {
            model:  'res.users',
            fields: ['name','company_id'],
            ids:    function(self){ return [session.uid]; },
            loaded: function(self,users){ self.user = users[0]; },
        },
        {
            model:  'res.company',
            fields: [ 'currency_id', 'email', 'street2', 'website', 'company_registry', 'vat', 'name', 'phone', 'partner_id' , 'country_id', 'tax_calculation_rounding_method', 'social_facebook', 'social_instagram'],
            ids:    function(self){ return [self.user.company_id[0]]; },
            loaded: function(self,companies){ self.company = companies[0]; },
        },
        {
            model:  'decimal.precision',
            fields: ['name','digits'],
            loaded: function(self,dps){
                self.dp  = {};
                for (var i = 0; i < dps.length; i++) {
                    self.dp[dps[i].name] = dps[i].digits;
                }
            },
        },
        {
            model:  'uom.uom',
            fields: [],
            domain: null,
            context: function(self){ return { active_test: false }; },
            loaded: function(self,units){
                self.units = units;
                _.each(units, function(unit){
                    self.units_by_id[unit.id] = unit;
                });
            }
        },
        {
            model:  'res.partner',
            fields: ['name','street','city','state_id','country_id','vat',
                     'phone','zip','mobile','email','barcode','write_date',
                     'property_account_position_id','property_product_pricelist'],
            domain: [['customer','=',true]],
            loaded: function(self,partners){
                self.partners = partners;
                self.db.add_partners(partners);
            },
        },
        {
            model:  'res.country',
            fields: ['name'],
            loaded: function(self,countries){
                self.countries = countries;
                self.company.country = null;
                for (var i = 0; i < countries.length; i++) {
                    if (countries[i].id === self.company.country_id[0]){
                        self.company.country = countries[i];
                    }
                }
            },
        },
        {
            model:  'account.tax',
            fields: ['name','amount', 'price_include', 'include_base_amount', 'amount_type', 'children_tax_ids', 'sequence'],
            domain: null,
            loaded: function(self, taxes){
                self.taxes = taxes;
                self.taxes_by_id = {};
                _.each(taxes, function(tax){
                    self.taxes_by_id[tax.id] = tax;
                });
                _.each(self.taxes_by_id, function(tax) {
                    tax.children_tax_ids = _.map(tax.children_tax_ids, function (child_tax_id) {
                        return self.taxes_by_id[child_tax_id];
                    });
                });
            },
        },
        {
            model:  'pos.session',
            fields: ['id', 'journal_ids','name','user_id','config_id','start_at','stop_at','sequence_number','login_number'],
            domain: function(self){ return [['state','=','opened'],['user_id','=',session.uid]]; },
            loaded: function(self,pos_sessions){
                self.pos_session = pos_sessions[0];
            },
        },
        {
            model: 'pos.config',
            fields: [],
            domain: function(self){ return [['id','=', self.pos_session.config_id[0]]]; },
            loaded: function(self,configs){
                self.config = configs[0];
                self.config.use_proxy = self.config.iface_payment_terminal ||
                                        self.config.iface_electronic_scale ||
                                        self.config.iface_print_via_proxy  ||
                                        self.config.iface_scan_via_proxy   ||
                                        self.config.iface_cashdrawer       ||
                                        self.config.iface_customer_facing_display;

                if (self.config.company_id[0] !== self.user.company_id[0]) {
                    throw new Error(_t("Error: The Point of Sale User must belong to the same company as the Point of Sale. You are probably trying to load the point of sale as an administrator in a multi-company setup, with the administrator account set to the wrong company."));
                }

                self.db.set_uuid(self.config.uuid);
                self.set_cashier(self.get_cashier());

                var orders = self.db.get_orders();
                for (var i = 0; i < orders.length; i++) {
                    self.pos_session.sequence_number = Math.max(self.pos_session.sequence_number, orders[i].data.sequence_number+1);
                }
           },
        },
        {
            model:  'res.users',
            fields: ['name','pos_security_pin','groups_id','barcode'],
            domain: function(self){ return [['company_id','=',self.user.company_id[0]],'|', ['groups_id','=', self.config.group_pos_manager_id[0]],['groups_id','=', self.config.group_pos_user_id[0]]]; },
            loaded: function(self,users){
                // we attribute a role to the user, 'cashier' or 'manager', depending
                // on the group the user belongs.
                var pos_users = [];
                for (var i = 0; i < users.length; i++) {
                    var user = users[i];
                    for (var j = 0; j < user.groups_id.length; j++) {
                        var group_id = user.groups_id[j];
                        if (group_id === self.config.group_pos_manager_id[0]) {
                            user.role = 'manager';
                            break;
                        } else if (group_id === self.config.group_pos_user_id[0]) {
                            user.role = 'cashier';
                        }
                    }
                    if (user.role) {
                        pos_users.push(user);
                    }
                    // replace the current user with its updated version
                    if (user.id === self.user.id) {
                        self.user = user;
                    }
                }
                self.users = pos_users;
            },
        },
        {
            model: 'stock.location',
            fields: [],
            ids:    function(self){ return [self.config.stock_location_id[0]]; },
            loaded: function(self, locations){ self.shop = locations[0]; },
        },
        {
            model:  'product.pricelist',
            fields: ['name', 'display_name'],
            domain: function(self) { return [['id', 'in', self.config.available_pricelist_ids]]; },
            loaded: function(self, pricelists){
                _.map(pricelists, function (pricelist) { pricelist.items = []; });
                self.default_pricelist = _.findWhere(pricelists, {id: self.config.pricelist_id[0]});
                self.pricelists = pricelists;
            },
        },
        {
            model:  'product.pricelist.item',
            domain: function(self) { return [['pricelist_id', 'in', _.pluck(self.pricelists, 'id')]]; },
            loaded: function(self, pricelist_items){
                var pricelist_by_id = {};
                _.each(self.pricelists, function (pricelist) {
                    pricelist_by_id[pricelist.id] = pricelist;
                });

                _.each(pricelist_items, function (item) {
                    var pricelist = pricelist_by_id[item.pricelist_id[0]];
                    pricelist.items.push(item);
                    item.base_pricelist = pricelist_by_id[item.base_pricelist_id[0]];
                });
            },
        },
        {
            model:  'product.category',
            fields: ['name', 'parent_id'],
            loaded: function(self, product_categories){
                var category_by_id = {};
                _.each(product_categories, function (category) {
                    category_by_id[category.id] = category;
                });
                _.each(product_categories, function (category) {
                    category.parent = category_by_id[category.parent_id[0]];
                });

                self.product_categories = product_categories;
            },
        },
        {
            model: 'res.currency',
            fields: ['name','symbol','position','rounding'],
            ids:    function(self){ return [self.config.currency_id[0]]; },
            loaded: function(self, currencies){
                self.currency = currencies[0];
                if (self.currency.rounding > 0) {
                    self.currency.decimals = Math.ceil(Math.log(1.0 / self.currency.rounding) / Math.log(10));
                } else {
                    self.currency.decimals = 0;
                }

            },
        },
        {
            model:  'pos.category',
            fields: ['id', 'name', 'parent_id', 'child_id'],
            domain: null,
            loaded: function(self, categories){
                self.db.add_categories(categories);
            },
        },
        {
            model:  'product.product',
            fields: ['display_name', 'list_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id',
                     'barcode', 'default_code', 'to_weight', 'uom_id', 'description_sale', 'description',
                     'product_tmpl_id','tracking'],
            order:  _.map(['sequence','default_code','name'], function (name) { return {name: name}; }),
            domain: [['sale_ok','=',true],['available_in_pos','=',true]],
            context: function(self){ return { display_default_code: false }; },
            loaded: function(self, products){
                self.db.add_products(_.map(products, function (product) {
                    product.categ = _.findWhere(self.product_categories, {'id': product.categ_id[0]});
                    return new exports.Product({}, product);
                }));
            },
        },
        {
            model:  'account.bank.statement',
            fields: ['account_id','currency_id','journal_id','state','name','user_id','pos_session_id'],
            domain: function(self){ return [['state', '=', 'open'],['pos_session_id', '=', self.pos_session.id]]; },
            loaded: function(self, cashregisters, tmp){
                self.cashregisters = cashregisters;

                tmp.journals = [];
                _.each(cashregisters,function(statement){
                    tmp.journals.push(statement.journal_id[0]);
                });
            },
        },
        {
            model:  'account.journal',
            fields: ['type', 'sequence'],
            domain: function(self,tmp){ return [['id','in',tmp.journals]]; },
            loaded: function(self, journals){
                var i;
                self.journals = journals;

                // associate the bank statements with their journals.
                var cashregisters = self.cashregisters;
                var ilen = cashregisters.length;
                for(i = 0; i < ilen; i++){
                    for(var j = 0, jlen = journals.length; j < jlen; j++){
                        if(cashregisters[i].journal_id[0] === journals[j].id){
                            cashregisters[i].journal = journals[j];
                        }
                    }
                }

                self.cashregisters_by_id = {};
                for (i = 0; i < self.cashregisters.length; i++) {
                    self.cashregisters_by_id[self.cashregisters[i].id] = self.cashregisters[i];
                }

                self.cashregisters = self.cashregisters.sort(function(a,b){
                    // prefer cashregisters to be first in the list
                    if (a.journal.type == "cash" && b.journal.type != "cash") {
                        return -1;
                    } else if (a.journal.type != "cash" && b.journal.type == "cash") {
                        return 1;
                    } else {
                        return a.journal.sequence - b.journal.sequence;
                    }
                });

            },
        },
        {
            model:  'account.fiscal.position',
            fields: [],
            domain: function(self){ return [['id','in',self.config.fiscal_position_ids]]; },
            loaded: function(self, fiscal_positions){
                self.fiscal_positions = fiscal_positions;
            }
        },
        {
            model:  'account.fiscal.position.tax',
            fields: [],
            domain: function(self){
                var fiscal_position_tax_ids = [];

                self.fiscal_positions.forEach(function (fiscal_position) {
                    fiscal_position.tax_ids.forEach(function (tax_id) {
                        fiscal_position_tax_ids.push(tax_id);
                    });
                });

                return [['id','in',fiscal_position_tax_ids]];
            },
            loaded: function(self, fiscal_position_taxes){
                self.fiscal_position_taxes = fiscal_position_taxes;
                self.fiscal_positions.forEach(function (fiscal_position) {
                    fiscal_position.fiscal_position_taxes_by_id = {};
                    fiscal_position.tax_ids.forEach(function (tax_id) {
                        var fiscal_position_tax = _.find(fiscal_position_taxes, function (fiscal_position_tax) {
                            return fiscal_position_tax.id === tax_id;
                        });

                        fiscal_position.fiscal_position_taxes_by_id[fiscal_position_tax.id] = fiscal_position_tax;
                    });
                });
            }
        },
        {
            label: 'fonts',
            loaded: function(){
                var fonts_loaded = new $.Deferred();
                // Waiting for fonts to be loaded to prevent receipt printing
                // from printing empty receipt while loading Inconsolata
                // ( The font used for the receipt )
                waitForWebfonts(['Lato','Inconsolata'], function(){
                    fonts_loaded.resolve();
                });
                // The JS used to detect font loading is not 100% robust, so
                // do not wait more than 5sec
                setTimeout(function(){
                    fonts_loaded.resolve();
                },5000);

                return fonts_loaded;
            },
        },
        {
            label: 'pictures',
            loaded: function(self){
                self.company_logo = new Image();
                var  logo_loaded = new $.Deferred();
                self.company_logo.onload = function(){
                    var img = self.company_logo;
                    var ratio = 1;
                    var targetwidth = 300;
                    var maxheight = 150;
                    if( img.width !== targetwidth ){
                        ratio = targetwidth / img.width;
                    }
                    if( img.height * ratio > maxheight ){
                        ratio = maxheight / img.height;
                    }
                    var width  = Math.floor(img.width * ratio);
                    var height = Math.floor(img.height * ratio);
                    var c = document.createElement('canvas');
                        c.width  = width;
                        c.height = height;
                    var ctx = c.getContext('2d');
                        ctx.drawImage(self.company_logo,0,0, width, height);

                    self.company_logo_base64 = c.toDataURL();
                    logo_loaded.resolve();
                };
                self.company_logo.onerror = function(){
                    logo_loaded.reject();
                };
                self.company_logo.crossOrigin = "anonymous";
                self.company_logo.src = '/web/binary/company_logo' +'?dbname=' + session.db + '&_'+Math.random();

                return logo_loaded;
            },
        },
        {
            label: 'barcodes',
            loaded: function(self) {
                var barcode_parser = new BarcodeParser({'nomenclature_id': self.config.barcode_nomenclature_id});
                self.barcode_reader.set_barcode_parser(barcode_parser);
                return barcode_parser.is_loaded();
            },
        }
    ]
//    load_server_data: function(){
//        var self = this;
//        var loaded = new $.Deferred();
//        var progress = 0;
//        var progress_step = 1.0 / self.models.length;
//        var tmp = {}; // this is used to share a temporary state between models loaders
//
//        function load_model(index){
//            if(index >= self.models.length){
//                loaded.resolve();
//            }else{
//                var model = self.models[index];
//                self.chrome.loading_message(_t('Loading')+' '+(model.label || model.model || ''), progress);
//
//                var cond = typeof model.condition === 'function'  ? model.condition(self,tmp) : true;
//                if (!cond) {
//                    load_model(index+1);
//                    return;
//                }
//
//                var fields =  typeof model.fields === 'function'  ? model.fields(self,tmp)  : model.fields;
//                var domain =  typeof model.domain === 'function'  ? model.domain(self,tmp)  : model.domain;
//                var context = typeof model.context === 'function' ? model.context(self,tmp) : model.context;
//                var ids     = typeof model.ids === 'function'     ? model.ids(self,tmp) : model.ids;
//                var order   = typeof model.order === 'function'   ? model.order(self,tmp):    model.order;
//                progress += progress_step;
//
//                if( model.model ){
//                    var params = {
//                        model: model.model,
//                        context: context,
//                    };
//
//                    if (model.ids) {
//                        params.method = 'read';
//                        params.args = [ids, fields];
//                    } else {
//                        params.method = 'search_read';
//                        params.domain = domain;
//                        params.fields = fields;
//                        params.orderBy = order;
//                    }
//
//                    rpc.query(params).then(function(result){
//                        try{    // catching exceptions in model.loaded(...)
//                            $.when(model.loaded(self,result,tmp))
//                                .then(function(){ load_model(index + 1); },
//                                      function(err){ loaded.reject(err); });
//                        }catch(err){
//                            console.error(err.stack);
//                            loaded.reject(err);
//                        }
//                    },function(err){
//                        loaded.reject(err);
//                    });
//                }else if( model.loaded ){
//                    try{    // catching exceptions in model.loaded(...)
//                        $.when(model.loaded(self,tmp))
//                            .then(  function(){ load_model(index +1); },
//                                    function(err){ loaded.reject(err); });
//                    }catch(err){
//                        loaded.reject(err);
//                    }
//                }else{
//                    load_model(index + 1);
//                }
//            }
//        }
//
//        try{
//            load_model(0);
//        }catch(err){
//            loaded.reject(err);
//        }
//
//        return loaded;
//    },

//    load_new_partners: function(){
//        var self = this;
//        var def  = new $.Deferred();
//        var fields = _.find(this.models,function(model){ return model.model === 'res.partner'; }).fields;
//        var domain = [['customer','=',true],['write_date','>',this.db.get_partner_write_date()]];
//        rpc.query({
//                model: 'res.partner',
//                method: 'search_read',
//                args: [domain, fields],
//            }, {
//                timeout: 3000,
//                shadow: true,
//            })
//            .then(function(partners){
//                if (self.db.add_partners(partners)) {   // check if the partners we got were real updates
//                    def.resolve();
//                } else {
//                    def.reject();
//                }
//            }, function(type,err){ def.reject(); });
//        return def;
//    },
//    on_removed_order: function(removed_order,index,reason){
//        var order_list = this.get_order_list();
//        if( (reason === 'abandon' || removed_order.temporary) && order_list.length > 0){
//            // when we intentionally remove an unfinished order, and there is another existing one
//            this.set_order(order_list[index] || order_list[order_list.length -1]);
//        }else{
//            // when the order was automatically removed after completion,
//            // or when we intentionally delete the only concurrent order
//            this.add_new_order();
//        }
//    },
//    get_cashier: function(){
//        return this.db.get_cashier() || this.get('cashier') || this.user;
//    },
//    // changes the current cashier
//    set_cashier: function(user){
//        this.set('cashier', user);
//        this.db.set_cashier(this.cashier);
//    },
//    get_client: function() {
//        var order = this.get_order();
//        if (order) {
//            return order.get_client();
//        }
//        return null;
//    },

	})

});
