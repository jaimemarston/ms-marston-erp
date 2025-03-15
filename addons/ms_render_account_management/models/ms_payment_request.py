from odoo import models, fields


class MsPaymentRequest(models.Model):
    _name = 'ms.payment.requests'
    _description = 'Pagos de solicitudes/Documentos'
    
    receipt_number = fields.Char('receipt number')
    date = fields.Date('date')
    details = fields.Text('details')
    amount = fields.Float('amount')
    request_id = fields.Many2one('ms.request.management', string='request')