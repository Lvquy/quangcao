# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    API_KEY = fields.Char(string='Api key custom search')
    SEARCH_ENGINE_ID = fields.Char(string='SEARCH ENGINE ID')
    of_user = fields.Char(string='Account google')
    create_date = fields.Date(string='Create date')

    @api.model
    def set_values(self):
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('quang_cao.API_KEY', self.API_KEY)
        ICP.set_param('quang_cao.SEARCH_ENGINE_ID', self.SEARCH_ENGINE_ID)
        ICP.set_param('quang_cao.of_user', self.of_user)
        ICP.set_param('quang_cao.create_date', self.create_date)

        super(ResConfigSetting, self).set_values()

    @api.model
    def get_values(self):
        ICP = self.env['ir.config_parameter'].sudo()
        res = super(ResConfigSetting, self).get_values()
        res['API_KEY'] = ICP.get_param('quang_cao.API_KEY')
        res['SEARCH_ENGINE_ID'] = ICP.get_param('quang_cao.SEARCH_ENGINE_ID')
        res['of_user'] = ICP.get_param('quang_cao.of_user')
        res['create_date'] = ICP.get_param('quang_cao.create_date')
        return res
