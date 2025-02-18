from odoo import models, fields, api

class ProjectPlan(models.Model):
    _name = 'ms_account_system.project_plan'
    _description = 'Project Plan'
    _order = 'name'

    projectplan_id = fields.Char(string='Codigo')
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")  # Descripción opcional

    active = fields.Boolean(string="Active", default=True)
    
    # Campos de auditoría (no es necesario declararlos, pero pueden ser usados)
    company_id = fields.Many2one(
    'res.company', string="Company", required=True, 
    default=lambda self: self.env.company)