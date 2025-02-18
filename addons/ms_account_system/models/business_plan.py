from odoo import models, fields

class BusinessPlan(models.Model):
    _name = 'ms_account_system.business_plan'
    _description = 'Plan de Rubros'
    _order = 'name'

    businessplan_id = fields.Char(string='Codigo')
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")  # Descripción opcional
    active = fields.Boolean(string="Active", default=True)
    
    company_id = fields.Many2one(
    'res.company', string="Company", required=True, 
    default=lambda self: self.env.company)