from odoo import models, fields

class msRequestSettings(models.Model):
    _name = 'ms.request.settings'
    _description = 'configuraciones para las solicitudes'
    
    name = fields.Char('name')
    type = fields.Selection([
        ('areas', 'areas')
    ], string='type')