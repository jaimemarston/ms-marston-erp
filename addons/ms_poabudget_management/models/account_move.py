# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    poa_activity_id = fields.Many2one("poa.activity", string="Activity")
