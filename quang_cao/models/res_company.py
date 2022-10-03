# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    list_email = fields.Many2many('res.users',string='List Email')