odoo.define('de_pos_measures_note.measures_notes', function (require) {
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

var _super_orderline = models.Orderline.prototype;
models.load_models({
        model: 'pos.order.measures',
        fields: ['name'],
        loaded: function (self, ordermeasures) {
            self.order_note_by_id = {};
            for (var i = 0; i < ordermeasures.length; i++) {
                self.order_note_by_id[ordermeasures[i].id] = ordermeasures[i];
            }
        }
    });
models.load_fields('pos.order.line','order_measure_note');

models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
        _super_orderline.initialize.call(this,attr,options);
        this.order_measure_note = this.order_measure_note || "";
    },
    set_measure_note: function(note){
        this.order_measure_note = note;
        this.trigger('change',this);
    },
    get_measure_note: function(note){
        return this.order_measure_note;
    },
    can_be_merged_with: function(orderline) {
        if (orderline.get_measure_note() !== this.get_measure_note()) {
            return false;
        } else {
            return _super_orderline.can_be_merged_with.apply(this,arguments);
        }
    },
    clone: function(){
        var orderline = _super_orderline.clone.call(this);
        orderline.order_measure_note = this.order_measure_note;
        return orderline;
    },
    export_as_JSON: function(){
        var json = _super_orderline.export_as_JSON.call(this);
        json.order_measure_note = this.order_measure_note;
        return json;
    },
    init_from_JSON: function(json){
        _super_orderline.init_from_JSON.apply(this,arguments);
        this.order_measure_note = json.order_measure_note;
    },
});

var MeasuresPopupWidget = PopupWidget.extend({
    count: 0,
    template: 'MeasuresPopupWidget',
    events: _.extend({}, PopupWidget.prototype.events, {
        'change .measure_temp': 'click_option'
        ),
        
    init: function (parent, options) {
        this.options = options || {};
        this._super(parent, _.extend({}, {
            size: "medium"
        }, this.options));
    },
    renderElement: function () {
        this._super();
        for (var measure in this.pos.order_note_by_id) {
            $('#measurement').append(this.pos.order_note_by_id[measure].name + "= ,\n")
        }
    },
    show: function (options) {
        options = options || {};
        this._super(options);
        //if(options.value){
            //   $('textarea').text(options.value);
        //}
    },
    click_confirm: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var line = this.pos.get_order().get_selected_orderline();
        line.set_measure_note($('#measurement').val());
        this.gui.close_popup();
    },
    click_option: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var old_text = $('#measurement').val();
        $('textarea').text(old_text);
    }

});

var OrderlineMeasureNoteButton = screens.ActionButtonWidget.extend({
    template: 'OrderlineMeasureNoteButton',
    button_click: function(){
        var line = this.pos.get_order().get_selected_orderline();
        if (line) {
            this.gui.show_popup('textarea',{
                title: _t('Add Measurement'),
                value:   line.get_measure_note(),
                confirm: function(note) {
                    line.set_measure_note(note);
                },
            });
        }
    },
});

screens.define_action_button({
    'name': 'orderline_measure_note',
    'widget': OrderlineMeasureNoteButton,
    'condition': function(){
        return this.pos.config.iface_orderline_order_measures_notes;
    },
});
return {
    OrderlineMeasureNoteButton: OrderlineMeasureNoteButton,
}
});
