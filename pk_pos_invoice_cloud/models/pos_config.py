# -*- coding: utf-8 -*-
import requests
import json
import random
from odoo import api, fields, models
import logging
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz
_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _compute_system_id(self):
        for rec in self:
            rec.pos_system_id = random.randint(1000000000, 9999999999)

    url = fields.Char(string='FBR URL')
    pos_system_id = fields.Char(string='System POS ID', compute='_compute_system_id')
    pos_machine_id = fields.Char(string='FBR POS ID')
    fbr_limit = fields.Float(string='FBR Limit')
    bearer = fields.Char(string="Bearer")
    local_url = fields.Char(string='Local Service URL')

class ResPartner(models.Model):
    _inherit = "res.partner"

    buyer_ntn = fields.Char(string='NTN')
    buyer_cnic = fields.Char(string='CNIC')

class PosJournal(models.Model):
    _inherit = "pos.payment.method"

    payment_mode = fields.Selection([('cash', 'Cash'), ('card', 'Card'),
                                     ('gift', 'Gift Voucher'), ('loyalty', 'Loyalty Card'),
                                     ('mixed', 'Mixed'), ('cheque', 'Cheque'),
                                ])

class PosOrder(models.Model):
    _inherit = 'pos.order'

    invoice_number = fields.Char(string='InvoiceNumber', copy=False)
    res_message = fields.Char(string="Response Message", copy=False)
    fbr_sync = fields.Boolean(string="FBR Sync", compute='_compute_fbr_sync')

    def _compute_fbr_sync(self):
        for order in self:
            order.fbr_sync = bool(order.invoice_number) and (order.res_message == 'Fiscal Invoice Number generated successfully.' or order.res_message == 'Invoice received successfully')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['invoice_number'] = ui_order['invoice_number']
        res['res_message'] = ui_order['res_message']
        return res

    def print_pos_receipt(self):
        res = super(PosOrder, self).print_pos_receipt()
        res['invoice_number'] = self.invoice_number
        return res

    def get_payment_type(self):
        try:
            payment_ids  = self.payment_ids.filtered(lambda x:x.payment_method_id and x.payment_method_id.payment_mode)
            if payment_ids:
                if len(payment_ids) > 1:
                    return 5
                else:
                    modes = payment_ids.mapped('payment_method_id.payment_mode')
                    dict_modes = {'cash': 1, 'card': 2, 'gift': 3, 'loyalty': 4, 'cheque': 6}
                    return dict_modes[modes[0]]
        except Exception as e:
            _logger.info('Payment Mode Error: %s', e)
        return 1

    def get_invoice_type(self):
        try:
            if self.amount_total >= 0:
                return 1
            else:
                return 3
        except Exception as e:
            _logger.info('Invoice Type Error: %s', e)
        return 1   

    def _prepare_pos_lines(self, lines):
        data = []
        total_discount = 0.0
        total_qty = 0.0
        total_sales = 0.0
        try:
            for line in lines:
                total_discount += round(abs(line.qty * ((line.price_unit * line.discount) / 100)), 2) or 0.0
                total_qty += abs(line.qty) or 0.0
                total_sales += abs(line.price_subtotal) or 0.0
                data.append({
                    "ItemCode": line.product_id.barcode or '',
                    "ItemName": line.product_id.name,
                    "Quantity": abs(line.qty) or 0.0,
                    "PCTCode":  line.product_id.product_tmpl_id.hs_code_id and line.product_id.product_tmpl_id.hs_code_id.hs_code or '',
                    "TaxRate":  line.tax_ids and abs(float(line.tax_ids[0].amount)) or 0.0, 
                    "SaleValue": abs(line.price_subtotal) or 0.0,
                    "TotalAmount": round(abs(line.price_subtotal_incl), 2) or 0.0,
                    "TaxCharged": round(abs(line.price_subtotal_incl) - abs(line.price_subtotal), 2) or 0.0,
                    "Discount": 0.0,
                    "FurtherTax": 0.0,
                    "InvoiceType": 3 if line.price_subtotal < 0 else 1,
                    "RefUSIN": '',
                })
        except Exception as e:
            _logger.info('Pos Line Creation Error: %s', e)
        return data, total_discount, total_qty, total_sales

    def _get_client_time(self):
        from datetime import datetime
        date = self.date_order.strftime('%Y-%m-%d %H:%M:%S')
        if date:
            user_tz = self.env.user.tz or self.env.context.get('tz') or 'UTC'
            local = pytz.timezone(user_tz)
            date = datetime.strftime(pytz.utc.localize(datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S")
        return date

    def send_invoice_data(self):
        print('CALLLLLLLLLLLLLLL')
        data = {}
        inv_response = {}
        if self.session_id and self.session_id.config_id and not self.invoice_number:
            lines, total_discount, total_qty, total_sales = self._prepare_pos_lines(self.lines)
            try:
                data.update({
                    "InvoiceNumber": '',
                    "POSID": self.session_id.config_id.pos_machine_id,
                    "USIN": self.pos_reference,
                    "DateTime": self._get_client_time(),
                    "BuyerNTN": self.partner_id.buyer_ntn if self.partner_id else '',
                    "BuyerCNIC": self.partner_id.buyer_cnic if self.partner_id else '',
                    "BuyerName": self.partner_id.name if self.partner_id else '',
                    "BuyerPhoneNumber": self.partner_id.phone if self.partner_id else '',
                    "TotalBillAmount": abs(self.amount_total) or 0.0,
                    "TotalTaxCharged": abs(self.amount_tax) or 0.0,
                    "TotalQuantity": total_qty or 0.0,
                    "TotalSaleValue": total_sales or 0.0,
                    "Discount": 0.0,
                    "FurtherTax": 0.0,
                    "PaymentMode": self.get_payment_type(),
                    "RefUSIN": '',
                    "InvoiceType": self.get_invoice_type(),
                    "items": lines,
                })
            except Exception as e:
                _logger.info('Data Creation Error: %s', e)
                return False
            try:
                header = {'Authorization': 'Bearer ' + self.session_id.config_id.bearer}
                response = requests.post(self.session_id.config_id.url, json=data, headers=header, verify=False)
                inv_response = response.json()
            except Exception as e:
                _logger.info('FBR Response Error: %s', e)
                return False
        self.update_pos_order(inv_response)
        if self.env.context.get('from_button'):
            return True
        else:
            return inv_response

    def update_pos_order(self, inv_response):
        if inv_response:
            inv_number = False
            fbr_sync = False
            try:
                if inv_response.get('InvoiceNumber'):
                    inv_number = inv_response.get('InvoiceNumber')
                self.write({'invoice_number': inv_number, 'res_message' : inv_response.get('Response', '')})
            except Exception as e:
                _logger.info('POS Order Error: %s', e)
                return False
        return True

    @api.model
    def fbr_call_from_cron(self):
        pos_orders = self.search([('invoice_number', '=', False)])
        for pos in pos_orders:
            pos.send_invoice_data()

    def refund(self):
        res = super(PosOrder, self).refund()
        if res.get('res_id'):
            self.browse(res.get('res_id')).send_invoice_data()
        return res