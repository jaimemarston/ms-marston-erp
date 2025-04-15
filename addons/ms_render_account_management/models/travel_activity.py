from odoo import models, fields, api


class TravelActivity(models.Model):
    _name = 'travel.activity'
    _description = 'Actividad de Viaje'

    name = fields.Char(string='Nombre de Actividad')
    request_id = fields.Many2one('ms.request.management', string='Solicitud de Viaje')
    project_id = fields.Many2one('account.analytic.account', string='Proyecto')
    activity_type = fields.Selection([
        ('viatic', 'Viáticos'),
        ('land', 'Pie Terrestre'),
        ('materials', 'Materiales'),
        ('air', 'Pie Aéreo'),
    ], string='Tipo de Actividad')
    amount = fields.Float(string='Monto', digits=(12, 2))
