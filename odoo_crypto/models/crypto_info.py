# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class CryptoInfo(models.Model):

    _name = "crypto.info"
    _description = "Crypto Info"

    name = fields.Char(string='Name')
    crypto_value_ids = fields.One2many(
        comodel_name="crypto.info.value",
        string="Crypto Values",
        inverse_name="crypto_id"

    )

class CryptoInfoValue(models.Model):

    _name = "crypto.info.value"
    _description = "Crypto Info Value"

    crypto_id = fields.Many2one(
        comodel_name="crypto.info",
        string="Crypto",
    )
    info_date = fields.Datetime(string='Info Date')
    value = fields.Float(
        string="Value"
    )

