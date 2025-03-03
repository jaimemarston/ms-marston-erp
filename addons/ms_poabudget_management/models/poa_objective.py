# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PoaObjective(models.Model):
    _name = "poa.objective"
    _description = "Objetivo Estratégico del POA"
    _inherit = ['portal.mixin', 'mail.alias.mixin.optional', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Objective Name", required=True)
    poa_id = fields.Many2one("poa.plan", string="Annual Operating Plan", required=True)
    poa_activity_ids = fields.One2many("poa.activity", "objective_id", string="Activities")
