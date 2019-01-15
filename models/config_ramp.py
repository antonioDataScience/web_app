# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from openerp.http import controllers_per_module
import requests
import json
from openerp.exceptions import Warning
from odoo.exceptions import UserError
from odoo import exceptions, _
from odoo.osv import osv


class ConfigRamp(models.Model):
    _name = "config.ramp"
    _rec_name = "ramp_number"

    ramp_number = fields.Integer('Ramp number', required=True)
    ramp_state = fields.Selection([('activated', 'Activated'),
                                    ('deactivated', 'Deactivated'),
                                   ('not_added', 'Not added')],default='not_added')

    state = fields.Selection([
        ('down', 'The Ramp is DOWN'),
        ('up', 'The Ramp is UP'),
        ('error', 'ERROR')],default='down')

    def activate(self):
        if self.ramp_state == "activated":
            raise osv.except_osv(('The ramp is already activated!'), ("Please calm down :) !"))
        if self.ramp_state == "deactivated" or self.ramp_state == "not_added":
            url = self.env['ir.values'].get_default('ramp.config.settings', 'AddRamp_url')
            r_put = requests.put(url, json={"RampId": self.ramp_number,
                                            "Action": "1",
                                            "User": "",
                                            "Latitude": "123",
                                            "Longitude": "243"})
        if r_put.status_code == 200 and json.loads(str(r_put._content))['Success']:
            self.ramp_state = 'activated'
        else:
            raise osv.except_osv(('ERROR!'), ("Something is not right!"))

    def deactivate(self):
        if self.ramp_state == "deactivated":
            raise osv.except_osv(('The ramp is already deactivated!'), ("Please calm down :) !"))
        if self.ramp_state == "activated" or self.ramp_state == "not_added":
            url = self.env['ir.values'].get_default('ramp.config.settings', 'RemoveRamp_url')
            r_delete = requests.delete(url, json={"RampId": self.ramp_number,
                                                  "Action": "0",
                                                  "User": "",
                                                  "Latitude": "123",
                                                  "Longitude": "243"})
            if r_delete.status_code == 200:
                self.ramp_state = 'deactivated'
                self.state = 'down'

        else:
            raise osv.except_osv(('ERROR!'), ("Something is not right!"))