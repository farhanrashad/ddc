odoo.define('de_pos_customer_balance.models', function (require) {
"use strict";
    
    var models = require('point_of_sale.models');
    models.load_fields('res.partner','credit');
});
	