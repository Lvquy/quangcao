# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class TeamUs(http.Controller):
    @http.route(['/team'], auth='public', website=True, csrf=False)
    def team(self, **kw):
        employee = request.env['hr.employee'].sudo().search([])
        values = {}
        values.update({
            'employee': employee,
        })

        return request.render('quang_cao.team', values)