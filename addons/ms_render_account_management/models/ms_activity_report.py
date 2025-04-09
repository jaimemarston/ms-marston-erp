from odoo import models, fields

class MSActivityReport(models.Model):
    _name = 'ms.activity.report'
    _description = 'Informe de Actividad'


    # Modelo para el Informe de Actividad (Formato 8)

    date = fields.Date(string="Fecha del Informe")
    report_number = fields.Char(string="N° Informe")
    author = fields.Char(string="Elabora")
    activity_name = fields.Char(string="Actividad")
    topic = fields.Char(string="Tema")
    school_name = fields.Char(string="Institución Educativa")
    location = fields.Char(string="Lugar")

    beneficiary_type = fields.Selection([
        ('general', 'General'),
        ('educational', 'Educativo'),
        ('health', 'Salud'),
    ], string="Tipo de beneficiario")
    women = fields.Integer(string="Mujeres")
    men = fields.Integer(string="Hombres")
    boys = fields.Integer(string="Niños")
    girls = fields.Integer(string="Niñas")
    total = fields.Integer(string="Total")

    advances = fields.Text(string="Avances")
    difficulties = fields.Text(string="Dificultades")
    suggestions = fields.Text(string="Sugerencias")
    comments = fields.Text(string="Observaciones")
    request_id = fields.Many2one('ms.request.management', string="Solicitud")
