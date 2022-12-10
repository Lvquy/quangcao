# -*- coding:utf8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    alow_cham_cong = fields.Boolean(string='Cho phép chấm công', default=True)
