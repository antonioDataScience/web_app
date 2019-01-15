# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class SystemConfig(models.TransientModel):
    _name = 'ramp.config.settings'
    _inherit = 'res.config.settings'

    InitAction_url = fields.Char(string="Init action", required=True)
    GetRampState_url = fields.Char(string="Get state", required=True)
    AddRamp_url = fields.Char(string="Add ramp", required=True)
    RemoveRamp_url = fields.Char(string="Remove ramp", required=True)
    recipients = fields.Char(string="Recipients")
    reply_to = fields.Char(string="Reply")


    @api.multi
    def set_InitAction_url_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ramp.config.settings', 'InitAction_url', self.InitAction_url)

    @api.multi
    def set_GetRampState_url_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ramp.config.settings', 'GetRampState_url', self.GetRampState_url)

    @api.multi
    def set_AddRamp_url_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ramp.config.settings', 'AddRamp_url', self.AddRamp_url)

    @api.multi
    def set_RemoveRamp_url_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ramp.config.settings', 'RemoveRamp_url', self.RemoveRamp_url)

    @api.multi
    def set_recipients_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ramp.config.settings', 'recipients', self.recipients)

    @api.multi
    def set_reply_to_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ramp.config.settings', 'reply_to', self.reply_to)

