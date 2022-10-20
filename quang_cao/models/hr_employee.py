# -*- coding:utf8 -*-
from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    alow_cham_cong = fields.Boolean(string='Cho phép chấm công', default=True)
    net_luong = fields.Integer(string='Lương cơ bản / tháng')
    luong_1cong = fields.Float(string='Lương 1 công', compute='compute_luong1cong')


    @api.onchange('net_luong')
    def compute_luong1cong(self):
        for rec in self:
            rec.luong_1cong = rec.net_luong /26

