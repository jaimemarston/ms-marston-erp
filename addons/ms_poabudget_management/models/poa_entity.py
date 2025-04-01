# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PoaEntity(models.Model):
    _name = "poa.entity"
    _description = "Entidad relacionada con el POA"
    _inherit = ['portal.mixin', 'mail.alias.mixin.optional', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Entity Name", required=True)
    code = fields.Char(string="Entity Code", required=True)
    address = fields.Char(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    responsible = fields.Char(string="Responsible")
    poa_activity_ids = fields.Many2many("poa.activity", string="Associated Activities")
