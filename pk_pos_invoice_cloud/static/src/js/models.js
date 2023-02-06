odoo.define('pk_pos_invoice_cloud.pk_pos_invoice_cloud', function(require) {
"use strict";
    var core = require('web.core');
    var _t = core._t;
    var models = require('point_of_sale.models');
    models.load_fields('pos.config', ['fbr_limit']);
    models.load_fields('pos.order', ['invoice_number']);
    models.load_fields('res.partner',['buyer_ntn', 'buyer_cnic']);
    models.load_fields('pos.payment.method', ['payment_mode']);

    models.load_models({
        model: 'hs.code',
        fields: ['hs_code', 'product_tmpl_ids'],
        domain: [],
        loaded: function(self, hs_codes){
            self.db.hs_codes = hs_codes;
        },
    });
    
    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function () {
            var res = _super_Order.export_for_printing.apply(this, arguments);
            var client  = this.get('client');
            res['invoice_number'] = this.invoice_number || '';
            res['res_message'] = this.res_message || '';
            res['buyer_ntn'] = client ? client.buyer_ntn : null
            res['buyer_cnic'] = client ? client.buyer_cnic : null
            res['client_phone'] = client ? client.phone : null
            return res;
        },
        export_as_JSON: function() {
            var data = _super_Order.export_as_JSON.apply(this, arguments);
            data.invoice_number = this.invoice_number || '';
            data.res_message = this.res_message || '';
            return data;
        },
        init_from_JSON: function(json) {
            this.invoice_number = json.invoice_number;
            this.res_message = json.res_message;
            _super_Order.init_from_JSON.call(this, json);
        },
    });
});
