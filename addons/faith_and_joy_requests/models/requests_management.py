from odoo import models, fields


class FajrRequestManagement(models.Model):
    _name = 'fajr.request.management'
    _description = 'Modelo para gestinar las solicitudes'


    name = fields.Char('name')
    description = fields.Text('description')
    request_type = fields.Selection([
        ('payment_client', 'Payment client'),
        ('payment_provider', 'Payment provider'),
        ('invoice_client', 'Invoice client'),
        ('invoice_provider', 'Invoice provider'),
    ], string='Request Type')
    