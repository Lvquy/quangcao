# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date
from odoo.exceptions import UserError


class ChamCong(models.Model):
    _name = 'cham.cong'
    _description = 'Chấm công nhân viên'
    _rec_name = 'ngay_cong'

    ngay_cong = fields.Date(string='Ngày công')
    state = fields.Selection([('0','Mới tạo'),('1','Đã xác nhận')],default='0', string='Trạng thái')
    nhan_vien = fields.One2many(comodel_name='line.nhanvien',inverse_name='ref_chamcong',string='Nhân viên')
    note = fields.Text(string='Ghi chú')
    tong_tangca = fields.Integer(string='Tổng thời gian tằng ca', compute='compute_total_tangca')
    total_employee = fields.Integer(string='Tổng nhân sự', compute='compute_total_em')
    ref_total_cong = fields.Many2one(comodel_name='total.cong', string='Ngày công trong tháng', domain=[('state','!=','1')])
    _sql_constraints = [
        ('ngay_cong_unique',
         'unique(ngay_cong)',
         'Đã tồn tại ngày công này!')
    ]

    def reload_emp(self):
        employee = self.env['hr.employee'].search([('department_id','!=',1)], order='department_id')
        list_em = []
        for i in employee:
            list_em.append((0, 0, {'employee_tp': i.id}))
        for rec in self:
            rec.nhan_vien = False
            rec.nhan_vien = list_em

    @api.onchange('nhan_vien')
    def compute_total_em(self):
        for rec in self:
            rec.total_employee = 0
            for em in rec.nhan_vien:
                rec.total_employee +=1

    def confirm(self):
        for rec in self:
            if rec.state == '0':
                rec.state = '1'
            else: raise UserError("Làm mới trình duyệt!")
    def cancel(self):
        for rec in self:
            if rec.state == '1':
                rec.state = '0'
            else: pass

    @api.model
    def default_get(self, fields):
        employee = self.env['hr.employee'].search([],order ='department_id')
        list_em = []
        ngay_trong_thang = self.env['total.cong'].search(['&',('state','!=','1'),('month','=',str(date.today().month))],limit=1)

        for i in employee:
            list_em.append((0, 0, {'employee_tp': i.id}))
        self = self.with_context(default_nhan_vien=list_em)
        self = self.with_context(default_ngay_cong = date.today())
        self = self.with_context(default_ref_total_cong = ngay_trong_thang.id)
        defaults = super(ChamCong, self).default_get(fields)
        return defaults

    @api.onchange('nhan_vien')
    def compute_total_tangca(self):
        for rec in self:
            rec.tong_tangca = 0
            for i in rec.nhan_vien:
                rec.tong_tangca += i.tangca

class LineNhanVien(models.Model):
    _name = 'line.nhanvien'
    _description = 'Line chấm công nhân viên'
    _rec_name = 'employee_tp'

    employee_tp = fields.Many2one(comodel_name='hr.employee', string='Nhân viên')
    sang = fields.Boolean(string='Sáng', default = True)
    chieu = fields.Boolean(string='Chiều', default = True)
    tangca = fields.Integer(string='Tăng ca (Phút)')
    note = fields.Text(string='Ghi chú')
    ref_chamcong = fields.Many2one(comodel_name='cham.cong', string='Ngày công')
    cong_trong_ngay = fields.Float(string='Công trong ngày',digits=(12,1), compute='compute_cong')

    @api.onchange('sang','chieu')
    def compute_cong(self):
        for rec in self:
            rec.cong_trong_ngay = 1
            if rec.sang == False:
                rec.cong_trong_ngay = rec.cong_trong_ngay - 0.5
            if rec.chieu == False:
                rec.cong_trong_ngay = rec.cong_trong_ngay - 0.5


class TotalCong(models.Model):
    _name = 'total.cong'
    _rec_name = 'month'
    _description = 'Tổng hợp ngày công cuối tháng để tính lương'
    _order = 'id desc'

    month = fields.Selection([
        ('0','Chọn tháng'),
        ('1','Tháng 1'),
        ('2','Tháng 2'),
        ('3','Tháng 3'),
        ('4','Tháng 4'),
        ('5','Tháng 5'),
        ('6','Tháng 6'),
        ('7','Tháng 7'),
        ('8','Tháng 8'),
        ('9','Tháng 9'),
        ('10','Tháng 10'),
        ('11','Tháng 11'),
        ('12','Tháng 12'),
    ],default=str(date.today().month),string='Tổng ngày công trong tháng')
    ngay_tao = fields.Date(string='Ngày tạo', default=date.today())
    nhan_vien = fields.One2many(comodel_name='line.nhanvien.total', inverse_name='ref_total_cong', string='Nhân viên')
    state = fields.Selection([('0','Mới tạo'),('1','Đã xác nhận')],default='0', string='Trạng thái')
    note = fields.Text(string='Ghi chú')
    list_cong = fields.One2many(comodel_name='cham.cong', inverse_name='ref_total_cong', string='Chi tiết từng ngày')


    def total_default_get(self):
        employee = self.env['hr.employee'].search([], order='department_id')
        list_em = []
        for i in employee:
            list_em.append((0, 0, {'employee_tp': i.id}))
        self.nhan_vien= False
        self.nhan_vien=list_em



    def confirm(self):
        self.state = '1'

    def cancel(self):
        self.state = '0'

    def compute_cong(self):
        for rec in self:
            tong_cong = {}
            tong_tangca = {}
            for line in rec.list_cong:
                for k in line.nhan_vien:
                    try:
                        tong_cong[k.employee_tp.id] += k.cong_trong_ngay
                        tong_tangca[k.employee_tp.id] += k.tangca
                    except KeyError:
                        tong_cong[k.employee_tp.id] = k.cong_trong_ngay
                        tong_tangca[k.employee_tp.id] = k.tangca
            for i in rec.nhan_vien:
                if i.employee_tp.id in tong_cong:
                    i.total_cong = tong_cong.get(i.employee_tp.id)
                if i.employee_tp.id in tong_tangca:
                    i.total_tangca = tong_tangca.get(i.employee_tp.id)





class LineNhanVienTotal(models.Model):
    _name = 'line.nhanvien.total'
    _rec_name = 'employee_tp'
    _description = 'List Employee'

    ref_total_cong = fields.Many2one(comodel_name='total.cong', string='Tổng công')
    employee_tp = fields.Many2one(comodel_name='hr.employee', string='Nhân viên')
    total_cong = fields.Float(string='Tổng công trong tháng')
    total_tangca = fields.Integer(string='Tổng thời gian tăng ca (Phút)')
    note = fields.Text(string='Ghi chú')