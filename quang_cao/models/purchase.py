# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date
from odoo.exceptions import UserError


class Purchase(models.Model):
    _inherit = 'purchase.order'
    _description = 'Inherit module purchase order'

    pay_date = fields.Date(string='Ngày trả tiền', tracking=True)
    overdue = fields.Date(string='Hạn chót trả tiền', tracking=True)
    state_payment = fields.Selection([('0', 'Chưa thanh toán'), ('1', 'Quá hạn'), ('2', 'Đã thanh toán đủ')],
                                     default='0',
                                     tracking=True,
                                     string='Trạng thái thanh toán')
    payment_lines = fields.One2many(comodel_name='purchase.payment', inverse_name='ref_pur',
                                    string='Thanh toán tiền')
    payed_total = fields.Integer(string='Số tiền đã thanh toán', compute='compute_payed_total')
    amount_total_coppy = fields.Monetary(string='Tổng tiền', related='amount_total')

    def compute_payed_total(self):
        for rec in self:
            rec.payed_total = 0
            for i in rec.payment_lines:
                rec.payed_total += i.acount_pay

    def confirm_payment(self):
        for rec in self:
            rec.pay_date = date.today()
            if rec.payed_total < rec.amount_total:
                raise UserError('Số tiền thanh toán chưa đủ,Hãy bổ sung thanh toán trước')
            rec.state_payment = '2'
            for l in rec.payment_lines:
                l.state = '1'

    def _check_overdue(self):
        # print('Cron job check overdue')
        today = date.today()
        Purchase = self.env['purchase.order'].search(['&',('overdue','!=',False),('state_payment','!=','2')])
        for i in Purchase:
            if today.day >= i.overdue.day and today.month >= i.overdue.month and today.year >= i.overdue.year:
                i.state_payment = '1'
                # print('qua han')
            else:
                i.state_payment = '0'
                # print('chua qua han')

    def get_pur_order_is_overdue_payment(self):
        for rec in self:
            Order_Overdule = rec.env['purchase.order'].search([('state_payment','=','1')])
            return Order_Overdule


    def cancel_payment(self):
        for rec in self:
            rec.state_payment = '0'
            rec.pay_date = False

    def _send_email(self):
        Company = self.env['res.company'].search([])
        for e in Company.list_email:
            # print(e.partner_id.email)
            # print('conjob send mail')
            template_id = self.env.ref('quang_cao.mail_template_purchase_overdue_payment')
            template_id.email_to = e.partner_id.email
            template = self.env['mail.template'].browse(template_id.id)
            template.send_mail(self.id, force_send=True)


class PurchasePayment(models.Model):
    _name = 'purchase.payment'

    pay_date = fields.Date(string='Ngày thanh toán', default=date.today())
    acount_pay = fields.Integer(string='Số tiền', default=1)

    ref_pur = fields.Many2one(comodel_name='purchase.order', string='Thanh toán cho đơn hàng')
    partner_id = fields.Many2one(comodel_name='res.partner',readonly=True, string='Tài khoản nguồn', default=lambda self: self.env.user.company_id.partner_id)
    to_acount = fields.Many2one(comodel_name='res.partner',related='ref_pur.partner_id',
                                string='Tài khoản thụ hưởng',store=True)
    state = fields.Selection([('0', 'Nháp'), ('1', 'Đã xác nhận')], string='Trạng thái', default='0')

    @api.onchange('acount_pay')
    def check_onchange_pay_count(self):
        for rec in self:
            if rec.acount_pay > rec.ref_pur.amount_total:
                raise UserError('Số tiền lớn hơn tổng cần thanh toán')
            if rec.acount_pay < 0:
                raise UserError('Số tiền phải lớn hơn 0')

    def unlink(self):
        if self.state == '1':
            raise UserError('Không được xóa chứng từ đã xác nhận')
        res = super(PurchasePayment, self).unlink()
        return res