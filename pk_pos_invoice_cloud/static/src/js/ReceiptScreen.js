odoo.define('pk_pos_invoice_cloud.ReceiptScreen', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const PkCloudReceiptScreen = ReceiptScreen => class extends ReceiptScreen {
        mounted() {
            // Here, we send a task to the event loop that handles
            // the printing of the receipt when the component is mounted.
            // We are doing this because we want the receipt screen to be
            // displayed regardless of what happen to the handleAutoPrint
            // call.
            setTimeout(async () => await this.handleAutoPrint(), 0);
            var order = this.env.pos.get_order();
            if (order.invoice_number) {
                jQuery("#qr-example").qrcode({
                    width: 100,
                    height: 100,
                    text: order.invoice_number
                });
            }
        }
    }

    Registries.Component.extend(ReceiptScreen, PkCloudReceiptScreen);

    return ReceiptScreen;
});
