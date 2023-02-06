odoo.define('pk_pos_invoice_cloud.PaymentScreen', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    var core = require('web.core');
    var _t = core._t;

    const PkCloudPaymentScreen = PaymentScreen => class extends PaymentScreen {
        async validateOrder(isForceValidate) {
            var order = this.env.pos.get_order();
            var customer = order.get_client();
            var self = this;
            if(this.env.pos.config.cash_rounding) {
                if(!this.env.pos.get_order().check_paymentlines_rounding()) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Rounding error in payment lines'),
                        body: this.env._t("The amount of your payment lines must be rounded to validate the transaction."),
                    });
                    return;
                }
            }
            if (order.get_total_paid() >= this.env.pos.config.fbr_limit && this.env.pos.config.fbr_limit > 0 && !order.get_client() && order.orderlines.length){
                return this.showPopup('ErrorPopup', {
                    title: _t('Customer not found'),
                    body:  _t('Please select customer before validating order !'),
                });
            }
            if (customer && customer.buyer_cnic === false && order.get_total_paid() >= this.env.pos.config.fbr_limit && this.env.pos.config.fbr_limit > 0) {
                return this.showPopup('ErrorPopup', {
                    title: _t('Customer CNIC Required'),
                    body:  _t('Please set CNIC in the customer !'),
                });
            }
            if (await this._isOrderValid(isForceValidate) && this.env.pos.config.local_url) {
                // remove pending payments before finalizing the validation
                for (let line of this.paymentLines) {
                    if (!line.is_done()) this.currentOrder.remove_paymentline(line);
                }
                var items = [];
                var total_qty = 0.0;
                var total_amount = 0.0;
                var advance_amt = 0.0;
                order.get_orderlines().forEach(function (line, index, array) {
                    var tax_rate = 0.0
                    total_qty += Math.abs(line.quantity);
                    line.get_taxes().forEach(function (tax, index, array) {
                        tax_rate += tax.amount
                    })
                    var hs_code = '';
                    self.env.pos.db.hs_codes.forEach(function(rec) {
                        if (rec.product_tmpl_ids.indexOf(line.product.product_tmpl_id) !== -1){
                            hs_code = rec.hs_code;
                        }
                    });
                    if (line.product.is_advance) {
                        advance_amt = Math.abs(line.get_price_without_tax()) || 0.0
                    }
                    else {
                        items.push({
                            "ItemCode": line.product.barcode || '',
                            "ItemName": line.product.display_name || '',
                            "Quantity": Math.abs(line.quantity) || 0.0,
                            "PCTCode": hs_code || '',
                            "TaxRate":  tax_rate || 0.0, 
                            "SaleValue": Math.abs(line.get_price_without_tax()) || 0.0,
                            "TotalAmount": line.get_price_with_tax() || 0.0,
                            "TaxCharged": Math.abs(line.get_tax()),
                            "Discount": 0.0,
                            "FurtherTax": 0.0,
                            "InvoiceType": 1,
                            "RefUSIN": '',
                        })
                        total_amount += line.get_price_with_tax();
                    }
                })
                var mode = 5;
                if (order.get_paymentlines().length >= 1) {
                    var all_modes = {'cash': 1, 'card': 2, 'gift': 3, 'loyalty': 4, 'cheque': 6};
                    order.get_paymentlines().forEach(function (line, index, array) {
                        mode = all_modes[line.payment_method.payment_mode];
                    })
                }
                var fbr_data = {
                    "InvoiceNumber": '',
                    "POSID": self.env.pos.config.pos_machine_id,
                    "USIN": order.name,
                    "DateTime": new Date().toLocaleString(),
                    "BuyerNTN": customer && customer.buyer_ntn || '',
                    "BuyerCNIC": customer && customer.buyer_cnic || '',
                    "BuyerName": customer && customer.name || '',
                    "BuyerPhoneNumber": customer && customer.phone || '',
                    "TotalBillAmount": Math.abs((order.get_total_with_tax() + advance_amt)).toFixed(2),
                    "TotalTaxCharged": Math.abs(order.get_total_tax()).toFixed(2),
                    "TotalQuantity": total_qty,
                    "TotalSaleValue": Math.abs((order.get_total_without_tax() + advance_amt)).toFixed(2),
                    "Discount": 0.0,
                    "FurtherTax": 0.0,
                    "PaymentMode": mode,
                    "RefUSIN": '',
                    "InvoiceType": total_amount > 0 ? 1: 3,
                    "items": items,
                }
                console.log('FBR DATA:::::::::::::;', fbr_data);
                if (fbr_data) {
                    $.ajax({
                        url: self.env.pos.config.local_url,
                        type: 'POST',
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify(fbr_data),
                        success: function(data) {
                            var invoice_number = data['InvoiceNumber'];
                            var res_message = data['Response']
                            order.invoice_number = invoice_number;
                            order.res_message = res_message;
                            setTimeout(function() {
                                self._finalizeValidation()
                            }, 500);
                        },
                        error: function(data) {
                            order.res_message = 'FBR Service not running';
                            order.invoice_number = '';
                            self._finalizeValidation()
                        }
                    });
                }
                else {
                    await self._finalizeValidation();
                }
            }
            else {
                super.validateOrder(...arguments);
            }
        }
    };

    Registries.Component.extend(PaymentScreen, PkCloudPaymentScreen);

    return PaymentScreen;
});
