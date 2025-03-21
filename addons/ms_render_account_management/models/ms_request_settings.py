from odoo import models, fields

class msRequestSettings(models.Model):
    _name = 'ms.request.settings'
    _description = 'Configuraciones para las solicitudes'
    
    name = fields.Char('name')
    type = fields.Selection([
        ('areas', 'areas'),
        ('service', 'Service'),
    ], string='type')