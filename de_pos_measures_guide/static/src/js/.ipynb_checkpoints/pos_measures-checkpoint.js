odoo.define('de_pos_measures_guide.pos_measures', function (require) {
    "use strict";
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var PopupWidget = require('point_of_sale.popups');
    var _t = core._t;
    var models = require('point_of_sale.models');
    
    var _super_orderline = models.Orderline.prototype;

    models.load_models({
        model: 'pos.order.measures',
        fields: ['name'],
        loaded: function (self, ordermeasures) {
            self.order_measures_by_id = {};
            for (var i = 0; i < ordermeasures.length; i++) {
                self.order_measures_by_id[ordermeasures[i].id] = ordermeasures[i];
            }
        }
    });
    models.load_fields('pos.order.line','measure_note');
    
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            this.measure_note = this.measure_note || "";
        },
        set_measure_note: function(note){
            this.measure_note = note;
            this.trigger('change',this);
        },
        get_measure_note: function(note){
            return this.measure_note;
        },
    });

    var MeasuresPopupWidget = PopupWidget.extend({
        count: 0,
        template: 'MeasuresPopupWidget',
        events: _.extend({}, PopupWidget.prototype.events, {
            'change .measure_temp': 'click_option'
        }),
        
        init: function (parent, options) {
            this.options = options || {};
            this._super(parent, _.extend({}, {
                size: "medium"
            }, this.options));
        },
        renderElement: function () {
            this._super();
            for (var measure in this.pos.order_measures_by_id) {
                $('#measurement').append(this.pos.order_measures_by_id[measure].name + "= \n")
                  //  .attr("id", this.pos.order_measures_by_id[note].id)
                  //  .attr("class", "note_option"))
                
                //$('#note_select').append($("<input type=text style=width:461;>" + "</input><br/>").attr("value", this.pos.order_measures_by_id[note].name)
                  //  .attr("id", this.pos.order_measures_by_id[note].id)
                  //  .attr("class", "note_option"))
            }
        },
        show: function (options) {
            options = options || {};
            this._super(options);
            $('textarea').text(options.value);
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
            //var e = document.getElementById("note_select");
            //var text = e.options[e.selectedIndex].value;
            //old_text += "\n";
            //old_text += text;
            $('textarea').text(old_text);
        }

    });
    gui.define_popup({name: 'measures_guide', widget: MeasuresPopupWidget});

    var ButtonMeasuresGuide = screens.ActionButtonWidget.extend({
        template: 'ButtonMeasuresGuide',
        button_click: function () {
            var line = this.pos.get_order().get_selected_orderline();
            if (line) {
                this.gui.show_popup('measures_guide', {
                    value: line.get_measure_note(),
                    'title': _t('Measurement Guide')
                });
            }
        }
    });

    screens.define_action_button({
        'name': 'pos_measures_guide',
        'widget': ButtonMeasuresGuide,
        'condition': function () {
            return this.pos.config.is_measures_guide;
        }
    });
});

