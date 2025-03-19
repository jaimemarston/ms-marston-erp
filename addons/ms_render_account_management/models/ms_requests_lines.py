from odoo import models, fields

import logging
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

    journal_id = fields.Many2one('account.journal', string='journal')

    def create(self, vals):
        record = super().create(vals)
        record.crear_asiento_contable(record.journal_id, record.document_type_id ,record.date, record.receipt_number, record.amount)
        return record
    
    def crear_asiento_contable(self, journal_id, document_id,fecha, referencia, monto, socio_id=False):
        # journal_id = self.env['account.journal'].search([('code', '=', 'MISC')])
        asiento = self.env['account.move'].create({
            'date': fecha,
            'ref': referencia,
            'render_account_id': self.request_id.id,
            'journal_id': journal_id.id,
            'l10n_latam_document_type_id': document_id.id,
            'l10n_latam_document_number': str(document_id.code) + str(self.id),
        })
        data = [
            {'move_id': asiento.id,
            'account_id': journal_id.default_account_id.id,
            'partner_id': socio_id,
            'debit': monto,
            'credit': 0.0,
            # 'tax_ids': [(6,0,[])],
            'name': 'Débito',},
            {'move_id': asiento.id,
            # 'account_id': cuenta_credito_id,
            'partner_id': socio_id,
            'debit': 0.0,
            # 'credit': monto,
            'name': 'Crédito',},
        ]
        self.env['account.move.line'].create(data)
        asiento.action_post()
        return asiento.id