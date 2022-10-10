# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date
from odoo.exceptions import UserError


class Sale(models.Model):
    _inherit = 'sale.order'
    _description = 'Inherit module sale'

    date_order = fields.Date(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    pay_date = fields.Date(string='Ngày trả tiền', tracking=True)
    overdue = fields.Date(string='Hạn chót trả tiền',tracking=True)
    state_payment = fields.Selection([('0','Chưa thanh toán'),('1','Quá hạn'),('2','Đã thanh toán đủ')], default='0',
                                     tracking=True,
                                     string='Trạng thái thanh toán')
    payment_lines = fields.One2many(comodel_name='sale.payment', inverse_name='ref_sale',
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

    def cancel_payment(self):
        for rec in self:
            rec.state_payment = '0'
            rec.pay_date = False

    def _check_overdue(self):
        print('Cron job check overdue')
        today = date.today()
        SaleOder = self.env['sale.order'].search(['&',('overdue','!=',False),('state_payment','!=','2'),('state','in',('sale','send','done'))])
        for i in SaleOder:
            if today.day >= i.overdue.day and today.month >= i.overdue.month and today.year >= i.overdue.year:
                i.state_payment = '1'
                print('qua han')
            else:
                i.state_payment = '0'
                print('chua qua han')


    def get_sale_order_is_overdue_payment(self):
        # push data to email template
        for rec in self:
            Order_Overdule = rec.env['sale.order'].search([('state_payment','=','1')])
            return Order_Overdule
    def _send_email(self):
        Company = self.env['res.company'].search([])

        sendmail = False
        check_sale = self.env['sale.order'].search([('state','in',('sale','sent','done'))])
        for i in check_sale:
            if i.state_payment == '1':
                self.sudo().write({'check_sendmail':True})
                sendmail = True
        if sendmail == True:
            for e in Company.list_email:
                print('conjob send mail')
                template_id = self.env.ref('quang_cao.mail_template_overdue_payment')
                template_id.email_to = e.partner_id.email
                template = self.env['mail.template'].browse(template_id.id)
                template.send_mail(self.id, force_send=True)
        else: pass

class SalePayment(models.Model):
    _name = 'sale.payment'

    pay_date = fields.Date(string='Ngày thanh toán', default=date.today())
    acount_pay = fields.Integer(string='Số tiền', default=1)


    ref_sale = fields.Many2one(comodel_name='sale.order',string='Thanh toán cho đơn hàng')
    partner_id = fields.Many2one(comodel_name='res.partner',string='Tài khoản nguồn', related='ref_sale.partner_id', store=True)
    to_acount = fields.Many2one(comodel_name='res.partner',default=lambda self:self.env.user.company_id.partner_id.id, string='Tài khoản thụ hưởng',readonly=True )
    state = fields.Selection([('0','Nháp'),('1','Đã xác nhận')], string='Trạng thái', default='0')

    @api.onchange('acount_pay')
    def check_onchange_pay_count(self):
        for rec in self:
            if rec.acount_pay > rec.ref_sale.amount_total:
                raise UserError('Số tiền lớn hơn tổng cần thanh toán')
            if rec.acount_pay < 0:
                raise UserError('Số tiền phải lớn hơn 0')

    def unlink(self):
        if self.state == '1':
            raise UserError('Không được xóa chứng từ đã xác nhận')
        res = super(SalePayment, self).unlink()
        return res
    # @api.model
    # def default_get(self, default_fields):
    #     default_source_account = 3
    #
    #     print('get default')
    #     contextual_self = self.with_context(default_source_account=default_source_account)
    #     return super(SalePayment, contextual_self).default_get(default_fields)
