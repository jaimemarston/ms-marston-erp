from odoo import models, fields

class MSConformityReport(models.Model):
    _name = 'ms.conformity.report'
    _description = 'Acta de Conformidad'

    #  Modelo para el Acta de Conformidad (Formato 9)

    supplier_name = fields.Char(string="Razón Social / Nombre")
    supplier_document_number = fields.Char(string="DNI / RUC")
    contact_info = fields.Text(string="Datos de Contacto")

    deliverable_description = fields.Text(string="Descripción del bien/servicio")
    quantity = fields.Integer(string="Cantidad")
    start_date = fields.Date(string="Fecha de inicio")
    end_date = fields.Date(string="Fecha de término")
    observations = fields.Text(string="Observaciones")

    response = fields.Text(string="Respuesta sobre cumplimiento")
    rating = fields.Selection([
        ('very_good', 'Muy bueno'),
        ('good', 'Bueno'),
        ('regular', 'Regular'),
    ], string="Calificación")

    service_ok = fields.Boolean(string="Características del servicio OK")
    deadline_ok = fields.Boolean(string="Plazo de entrega OK")
    content_ok = fields.Boolean(string="Contenido del servicio OK")
    other_ok = fields.Boolean(string="Otro aspecto OK")
    request_id = fields.Many2one('ms.request.management', string="Solicitud")