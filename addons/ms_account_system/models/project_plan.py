from odoo import models, fields

class ProjectPlan(models.Model):
    _name = 'ms_account_system.project_plan'
    _description = 'Plan de Proyectos'
    _order = 'sequence, name'

    projectplan_id = fields.Char(string='Codigo')
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")  # Descripción opcional

    currency_type = fields.Char(string='Currency Type', size=3)
    
    # Campos de auditoría (no es necesario declararlos, pero pueden ser usados)
    create_uid = fields.Many2one('res.users', string="Created by", readonly=True)
    create_date = fields.Datetime(string="Creation Date", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Modified by", readonly=True)
    write_date = fields.Datetime(string="Last Modified on", readonly=True)
    Company_id = fields.Many2one(
    'res.company', string="Company", required=True, 
    default=lambda self: self.env.company,
    active = fields.Boolean(string="Active", default=True),
    sequence = fields.Integer(string="Sequence", default=10),
    user_id = fields.Many2one('res.users', string="Assigned to")

    )