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
import datetime
import time


class WebApplication(models.Model):
    _name = 'web.application'

    name = fields.Char("Name", required=True)
    surname = fields.Char("Surname", required=True)
    ramp_street_location = fields.Char("Street")
    ramp_city = fields.Char("City" )
    ramp_country = fields.Many2one('res.country',"City")
    user_id = fields.Many2one('res.users', string="Ramp user", track_visibility='onchange',default=lambda self: self.env.user)
    # ramp_state = fields.Selection([('activated', 'Activated'),
    #                                 ('deactivated', 'Deactivated')],
    #                                 default='deactivated')
    ramp_state = fields.Char("Ramp state", compute='_change_ramp_state')
    # state = fields.Char("State", compute='_change_position')
    current_user = fields.Boolean('is current user ?', compute='_get_current_user')
    ramp_id = fields.Integer("ramp_id")
    RAMP_ID = fields.Many2one('config.ramp', string="RAMP_ID", required=True)
    state = fields.Selection([
        ('down', 'The Ramp is DOWN'),
        ('up', 'The Ramp is UP'),
        ('error', 'ERROR')],default='down',compute='_change_position')


    @api.multi
    @api.onchange('RAMP_ID','RAMP_ID.ramp_state')
    def _change_ramp_state(self):
        for ramp in self:
            ramp.ramp_state = ramp.RAMP_ID.ramp_state

    @api.multi
    @api.onchange('RAMP_ID','RAMP_ID.state')
    def _change_position(self):
        for ramp in self:
            ramp.state = ramp.RAMP_ID.state


    @api.depends('user_id')
    def _get_current_user(self):
        for e in self:
            e.current_user = (True if e.env.user.id == e.user_id.id and e.env.user.id != 1 else False)

    def new_post_up(self):
        if self.RAMP_ID.ramp_state == "deactivated" or self.RAMP_ID.ramp_state == "not_added":
            raise exceptions.except_orm(_('The ramp is not active.'), _("Admin should activate the ramp!"))
        if self.RAMP_ID.state == 'up':
            raise osv.except_osv(('Repeated action'), ("The ramp is already UP!"))
        if self.RAMP_ID.state == 'error':
            raise osv.except_osv(('Error occured'), ("Please press ALERT!"))
        url = self.env['ir.values'].get_default('ramp.config.settings', 'InitAction_url')
        r_post = requests.post(url, json={"RampId": self.RAMP_ID.ramp_number,
                                          "Action": "1",
                                          "User": "",
                                          "Latitude": "123",
                                          "Longitude": "243"})

        if r_post.status_code == 200 and json.loads(str(r_post._content))['Success']:
            self.RAMP_ID.state = 'up'
            time.sleep(3)

        else:
            self.RAMP_ID.state = "error"


    def new_post_down(self):
        if self.RAMP_ID.ramp_state == "deactivated" or self.RAMP_ID.ramp_state == "not_added":
            raise exceptions.except_orm(_('The ramp is not active.'), _("Admin should activate the ramp!"))
        if self.RAMP_ID.state == 'down':
            raise exceptions.except_orm(_('Repeated action'), _("The ramp is already DOWN!"))
        if self.RAMP_ID.state == 'error':
            raise osv.except_osv(('Error occured'), ("Please press ALERT!"))
        url = self.env['ir.values'].get_default('ramp.config.settings', 'InitAction_url')
        r_post = requests.post(url, json={"RampId": self.RAMP_ID.ramp_number,
                                          "Action": "0",
                                          "User": "",
                                          "Latitude": "123",
                                          "Longitude": "243"})


        if r_post.status_code == 200 and json.loads(str(r_post._content))['Success']:
            self.RAMP_ID.state = 'down'
            time.sleep(3)

        else:
            self.RAMP_ID.state = "error"

    def get_state(self):
            url = self.env['ir.values'].get_default('ramp.config.settings', 'GetRampState_url')
            r_state = requests.post(url, json={"RampId": self.RAMP_ID.ramp_number,
                                               "Action": 0,
                                               "User": "",
                                               "Latitude": "123",
                                               "Longitude": "243"})
            return json.loads(r_state.content)['Action']


    def send_mail(self):
        recipients = self.env['ir.values'].get_default('ramp.config.settings', 'recipients')
        if not recipients:
            return
        reply_to = self.env['ir.values'].get_default('ramp.config.settings', 'reply_to')
        temp = str(datetime.datetime.now())[:19]
        temp = temp.replace(":", "_")
        template_obj = self.env['mail.mail']
        template_data = {
            'subject': 'Error at ' + temp,
            'body_html': "Something is not right with the ramp " + str(self.RAMP_ID.ramp_number) +"." + "<br> User: " + self.env.user.name,
            'email_from': reply_to,
            'email_to': recipients
        }
        template_id = template_obj.create(template_data)
        template_obj.send(template_id)

    @api.multi
    @api.onchange('RAMP_ID','RAMP_ID.ramp_state')
    def change_colore_on_kanban(self):
        for record in self:
            # position = record.get_state()
            # if record.state == 'deactivated':
            #     color = 1
            #     record.color = color
            #     break
            # if record.state == 'error':
            #     record.color = 2
            #     break
            # if not position:
            #     record.color = 5
            # else:
            #     record.color = 8
            record.color = 0

    color = fields.Integer('Color Index', compute="change_colore_on_kanban")