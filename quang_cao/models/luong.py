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
    state = fields.Selection([('0','Nháp'),('1','Đã chuyển tiền',)],default='0', string='Trạng thái')
    status = fields.Boolean(string='Đã trả đủ', default=False)
    ref_ung_luong = fields.Many2one(comodel_name='total.cong', string='Ứng lương trong tháng', readonly=True)

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
            print(rec.ref_ung_luong.id)
            if rec.ref_ung_luong.id == False:
                raise UserError('Không được tạo ở đây, vào tổng hợp cuối tháng chọn tab ứng lương để tạo')

    def cancel(self):
        for rec in self:
            if rec.state == '1':
                rec.state = '0'
            else: raise UserError('Làm mới trình duyệt')

    def unlink(self):
        for rec in self:
            if rec.state == '1':
                raise UserError('Không thể xoá khi đã xác nhận')
            else:
                return super(UngLuong, self).unlink()