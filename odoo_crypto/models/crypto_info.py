# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json
import logging
from odoo import SUPERUSER_ID
from lxml import etree

class CryptoInfo(models.Model):

    _name = "crypto.info"
    _description = "Crypto Info"

    name = fields.Char(string='Name')
    symbol = fields.Char(string='Symbol')
    external_id = fields.Integer(string='External ID')
    crypto_value_ids = fields.One2many(
        comodel_name="crypto.info.value",
        string="Crypto Values",
        inverse_name="crypto_id"

    )

    def cron_crypto_info(self):
        model_obj = self.env[self._name]
        ir_config = self.env['ir.config_parameter']
        total_coins = 0
        limit = 100
        start_coin_num = 0
        # Info global API
        api_url_global = ir_config.get_param('API_URL_GLOBAL')
        resp_global = requests.get(api_url_global)
        res_text = json.loads(resp_global.text)
        total_coins = int(res_text[0]['coins_count'])
        # Info coins API
        api_url_info = ir_config.get_param('API_URL_INFO')
        coin_actual = start_coin_num
        while total_coins > 0:
            text_format = '?start={}&limit{}'.format(coin_actual, limit)
            api_url_complete = api_url_info + text_format
            resp = requests.get(api_url_complete)
            res_text = json.loads(resp.text)
            data = res_text['data'] if res_text.get('data') else ''
            if not data:
                continue
            model_obj.create_values(data, model_obj)
            coin_actual += limit
            total_coins -= limit
        
    
    def create_values(self, data, model_obj):
        for dat in data:
            value_model = model_obj.search([('external_id', '=', int(dat['id']))])
            if not value_model:
                dict_value = {
                    'name': dat['name'],
                    'symbol': dat['symbol'],
                    'external_id': int(dat['id']),

                }
                value_model = model_obj.create(dict_value)
            try:
                value_info = {
                    'info_date': fields.Datetime.now(),
                    'value': dat['price_usd']
                }
                logging.error(value_info)
                value_model.write({'crypto_value_ids': [(0, 0, value_info)]}) 
            except Exception as exc:
                logging.error(exc)
                continue

            

class CryptoInfoValue(models.Model):

    _name = "crypto.info.value"
    _description = "Crypto Info Value"

    crypto_id = fields.Many2one(
        comodel_name="crypto.info",
        string="Crypto",
    )
    info_date = fields.Datetime(string='Info Date')
    value = fields.Float(
        string="Value",
        digits=(20,6),
        help='Always in USD'
    )
    """value_currency_user = fields.Float(
        string="Value Currency",
        digits=(20,6),
        help='Value in your currency',
        compute='_compute_currency_user'
    )
    

    def _compute_currency_user(self):
        currency_user = self.env.user.currency_id
        currency_usd = self.env['res.currency'].search([('name', '=', 'USD')])
        for value in self:
            value.value_currency_user = currency_usd.with_context(date=value.info_date.date()).compute(value.value, currency_user.id)"""
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):

        res = super(CryptoInfoValue, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        if view_type != 'search' and self.env.uid != SUPERUSER_ID:
            root = etree.fromstring(res['arch'])
            root.set('create', 'false')
            root.set('edit', 'false')
            res['arch'] = etree.tostring(root)
        return res

