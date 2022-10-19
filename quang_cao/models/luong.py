# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date
from odoo.exceptions import UserError

class UngLuong(models.Model):
    _name = 'ung.luong'
    _description = 'Ứng lưng nhân viên, chi tiêu vật tư'
    _rec_name = 'ma_phieu'

    ma_phieu = fields.Char(string='Mã phiếu',readonly=True, default=lambda self: 'New')
    ngay_ung = fields.Date(string='Ngày ứng' , default=date.today())
    nguoi_ung = fields.Many2one(comodel_name='hr.employee', string='Người ứng')
    chung_tu = fields.Text(string='Chứng từ chuyển khoản')
    so_tien = fields.Integer(string='Số tiền ứng(VNĐ)')
    type_ung = fields.Selection([('0','Chọn kiểu ứng'),('luong','Ứng lương'),('vl','Ứng mua vật liệu')],default='0',string='Kiểu ứng')
    note = fields.Text(string='Lý do ứng')
    state = fields.Selection([('0','Nháp'),('1','Đã chuyển',)],default='0', string='Trạng thái')
    status = fields.Boolean(string='Đã trả đủ', default=False)

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New' == 'New'):
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('maphieu.code') or 'New'
            res = super(UngLuong, self).create(vals)
        return res

    def confirm(self):
        for rec in self:
            if rec.state == '0':
                rec.state = '1'
            else: raise UserError('Làm mới trin duyệt')

    def cancel(self):
        for rec in self:
            if rec.state == '1':
                rec.state = '0'
            else: raise UserError('Làm mới trình duyệt')