# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PoaActivity(models.Model):
    _name = "poa.activity"
    _description = "Actividad del POA"
    _inherit = ['portal.mixin', 'mail.alias.mixin.optional', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name of the Activity", required=True)
    code = fields.Char(string="Activity Code", required=True)
    objective_id = fields.Many2one("poa.objective", string="Goal", required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    budget_ids = fields.One2many("poa.budget", "poa_activity_id", string="Budgets")
    invoice_ids = fields.One2many("account.move", "poa_activity_id", string="Related Invoice")
    analytic_account_id = fields.Many2one("account.analytic.account", string="Analytic Account")
    entity_ids = fields.Many2many("poa.entity", string="Entities where executed")
