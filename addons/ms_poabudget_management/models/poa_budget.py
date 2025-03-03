# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PoaBudget(models.Model):
    _name = "poa.budget"
    _description = "Presupuestos"
    _rec_name = "name"
    _inherit = ['portal.mixin', 'mail.alias.mixin.optional', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name of Budget", required=True)
    poa_activity_id = fields.Many2one("poa.activity", string="Activity")
