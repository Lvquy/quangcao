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

    @http.route(['/dieu-khoan'], auth='public', website=True)
    def dieu_khoan(self, **kw):

        return request.render('quang_cao.dieu_khoan')

    @http.route(['/bien-quang-cao-dep'], auth='public', website=True)
    def bien_quang_cao_dep(self, **kw):

        return request.render('quang_cao.bien_quang_cao_dep')


    @http.route(['/bang-gia-bien-quang-cao'], auth='public', website=True)
    def bang_gia(self, **kw):

        return request.render('quang_cao.bang_gia_bien_quang_cao')