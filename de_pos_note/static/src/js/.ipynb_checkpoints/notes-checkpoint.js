odoo.define('de_pos_note.notes', function (require) {
"use strict";

var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');

var QWeb = core.qweb;
var _t   = core._t;

var _super_orderline = models.Orderline.prototype;
models.load_fields('pos.order.line','order_note');

models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
        _super_orderline.initialize.call(this,attr,options);
        this.order_note = this.order_note || "";
    },
    set_note: function(note){
        this.order_note = note;
        this.trigger('change',this);
    },
    get_note: function(note){
        return this.order_note;
    },
    can_be_merged_with: function(orderline) {
        if (orderline.get_note() !== this.get_note()) {
            return false;
        } else {
            return _super_orderline.can_be_merged_with.apply(this,arguments);
        }
    },
    clone: function(){
        var orderline = _super_orderline.clone.call(this);
        orderline.order_note = this.order_note;
        return orderline;
    },
    export_as_JSON: function(){
        var json = _super_orderline.export_as_JSON.call(this);
        json.order_note = this.order_note;
        return json;
    },
    init_from_JSON: function(json){
        _super_orderline.init_from_JSON.apply(this,arguments);
        this.order_note = json.order_note;
    },
});

var OrderlineNoteButton1 = screens.ActionButtonWidget.extend({
    template: 'OrderlineNoteButton1',
    button_click: function(){
        var line = this.pos.get_order().get_selected_orderline();
        if (line) {
            this.gui.show_popup('textarea',{
                title: _t('Add Note'),
                value:   line.get_note(),
                confirm: function(note) {
                    line.set_note(note);
                },
            });
        }
    },
});

screens.define_action_button({
    'name': 'orderline_note',
    'widget': OrderlineNoteButton1,
    'condition': function(){
        return this.pos.config.iface_orderline_notes;
    },
});
return {
    OrderlineNoteButton1: OrderlineNoteButton1,
}
});
