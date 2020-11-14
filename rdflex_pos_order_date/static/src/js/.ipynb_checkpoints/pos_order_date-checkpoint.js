odoo.define('pos_order_date', function (require) {
"use strict";
var screens = require('point_of_sale.screens');
var posModel = require('point_of_sale.models');
var fieldUtils = require('web.field_utils');

var PaymentScreenWidget = screens.PaymentScreenWidget;
PaymentScreenWidget.include({
    renderElement: function () {
        this._super.apply(this, arguments);
        this.$('#order_date_picker').datepicker({
            showOn: "button",
            buttonImage: "/rdflex_pos_order_date/static/img/calendar.gif",
            buttonImageOnly: true,
            buttonText: "Select date"
        });
    },
        
    get_order_date() {
        var orderDate = this.$('#order_date_picker').datepicker('getDate');
        return orderDate || new Date();

    },
    finalize_validation: function () {
        var self = this;
        var order = this.pos.get_order();
        if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) { 

                this.pos.proxy.open_cashbox();
        }
        var orderDate = this.get_order_date();
        order.initialize_validation_post_date(orderDate);
        order.finalized = true;

        if (order.is_to_invoice()) {
            var invoiced = this.pos.push_and_invoice_order(order);
            this.invoicing = true;

            invoiced.fail(this._handleFailedPushForInvoice.bind(this, order, false));

            invoiced.done(function () {
                self.invoicing = false;
                self.gui.show_screen('receipt');
            });
        } else {
            this.pos.push_order(order);
            this.gui.show_screen('receipt');
        }
    },
});

posModel.Order = posModel.Order.extend({
    initialize_validation_post_date: function (date) {
        this.validation_date = date;
        this.formatted_validation_date = fieldUtils.format.datetime(
            moment(this.validation_date), {}, {timezone: false});
    }
});

});
