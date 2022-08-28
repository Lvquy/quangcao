# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class QuangCao(http.Controller):
    @http.route(['/team'], auth='public', website=True)
    def team(self, **kw):
        # employee = request.env['hr.employee'].sudo().search([])
        # values = {}
        # values.update({
        #     'employee': employee,
        # })

        return request.render('quang_cao.team')

    @http.route(['/dieu_khoan'], auth='public', website=True)
    def dieu_khoan(self, **kw):

        return request.render('quang_cao.dieu_khoan')

    @http.route(['/bien_quang_cao_dep'], auth='public', website=True)
    def bien_quang_cao_dep(self, **kw):

        return request.render('quang_cao.bien_quang_cao_dep')