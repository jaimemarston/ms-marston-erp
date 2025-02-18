from odoo import models, fields

class FinancialPlan(models.Model):
    _name = 'ms_account_system.activity_plan'
    _description = 'Plan de Activades'
    _order = 'name'

    financialplan_id = fields.Char(string='Codigo')
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")  # Descripción opcional
    active = fields.Boolean(string="Active", default=True)
    
    # Campos de auditoría (no es necesario declararlos, pero pueden ser usados)
    company_id = fields.Many2one(
    'res.company', string="Company", required=True, 
    default=lambda self: self.env.company)