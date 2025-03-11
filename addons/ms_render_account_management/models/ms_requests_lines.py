from odoo import models, fields


class MsRequestsLines(models.Model):
    _name = 'ms.requests.lines'
    _description = 'Lineas de solicitudes'
    

    partner_id = fields.Many2one('res.partner', string='partner')
    document_type_id = fields.Many2one('l10n_latam.document.type', string='document type')
    series = fields.Char('series')
    receipt_number = fields.Char('receipt number')
    date = fields.Date('date')
    details = fields.Text('details')
    amount = fields.Float('amount')
    request_id = fields.Many2one('ms.request.management', string='request')
    rate = fields.Float('Rate', digits=(16, 3))
    transaction_date = fields.Date('Transaction date')
    transaction_number = fields.Char('Transaction number')
    res_currency_id = fields.Many2one('res.currency', string='Currency')
    due_date = fields.Date('Due date')
    retention = fields.Boolean('Retention')