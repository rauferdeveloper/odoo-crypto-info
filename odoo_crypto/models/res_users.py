# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class User(models.Model):

    _inherit = "res.users"

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency"
    )    