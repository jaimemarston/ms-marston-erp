# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PoaPlan(models.Model):
    _name = "poa.plan"
    _description = "Plan Operativo Anual"
    _rec_name = "name"
    _inherit = ['portal.mixin', 'mail.alias.mixin.optional', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name of POA", required=True)
    year = fields.Integer(string="Year", required=True)
    objective_ids = fields.One2many("poa.objective", "poa_id", string="Goals")
