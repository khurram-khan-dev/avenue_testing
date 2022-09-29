# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class invoiceExtension(models.Model):
    _inherit = 'account.move'
    word_num = fields.Char(string = "Amount In Words:", compute = '_amount_in_word')
    def _amount_in_word(self): 
        for rec in self: 
            rec.word_num = str(rec.currency_id.amount_to_text(rec.amount_total)) 
