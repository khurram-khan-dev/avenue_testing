# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class FbrWizard(models.TransientModel):
    _name = 'fbr.wizard'
    _description = 'Change FBR mode wizard'

    url = fields.Char(string='URL')

    def action_fbr_change(self):
        # https://makeameme.org/meme/i-am-your-uvzw4a
        self.env.cr.execute('update pos_config set url=%s', [self.url])
        return {'type': 'ir.actions.act_window_close'}
