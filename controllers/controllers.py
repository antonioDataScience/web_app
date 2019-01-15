# -*- coding: utf-8 -*-
import odoo.http as http

class your_class(http.Controller):
     @http.route('/web_app', type='http', auth='user', website=True)
     def show_custom_webpage(self, **kw):
          return http.request.render('web_app.login', {})