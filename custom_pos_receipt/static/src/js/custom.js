odoo.define('custom_pos_receipt.pos_order_extend', function (require) {
"use strict";
   var models = require('point_of_sale.models');
   var screens = require('point_of_sale.screens');
   var core = require('web.core');
   var QWeb = core.qweb;
   var exports = {};

   var _super_posmodel = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            // New code
            var partner_model = _.find(this.models, function(model){
                return model.model === 'res.company';
            });
            partner_model.fields.push('street', 'street2', 'city');

            // Inheritance
            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });

   models.load_fields('pos.order',['invoice_number']);
});