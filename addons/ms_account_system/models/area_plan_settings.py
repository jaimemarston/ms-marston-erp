from odoo import models, fields

class msRequestSettings(models.Model):
    _name = 'ms.account.system.settings'
    _description = 'Configuraciones para las areas'
    
    name = fields.Char('Name')
    type = fields.Selection([
        ('areas', 'Areas'),
        ('service', 'Service'),
    ], string='Type')

    description = fields.Text(string="Description")
    active = fields.Boolean('Active', default=True)
