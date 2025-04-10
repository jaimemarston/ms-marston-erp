from odoo import api, fields, models, Command, _


class MsRequestsLines(models.Model):
    _name = 'ms.requests.lines'
    _description = 'Lineas de solicitudes'

    partner_id = fields.Many2one('res.partner', string='partner')
    document_type_id = fields.Many2one('l10n_latam.document.type', string='document type')
    series = fields.Char('series')
    receipt_number = fields.Char('receipt number')
    date = fields.Date('date',default=fields.Date.context_today)
    details = fields.Text('details')
    amount = fields.Float('amount', compute='_compute_amount')
    request_id = fields.Many2one('ms.request.management', string='request')
    rate = fields.Float('Rate', digits=(16, 3))
    transaction_date = fields.Date('Transaction date')
    transaction_number = fields.Char('Transaction number')
    res_currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'PEN')], limit=1).id)
    due_date = fields.Date('Due date')
    retention = fields.Boolean('Retention')
    has_additional_cost = fields.Boolean('¿Costo adicional por entrega?')
    additional_delivery_cost = fields.Float('Monto de costo adicional', digits=(16, 2))
    unit_price = fields.Float('Precio Unitario') 
    cant_product = fields.Integer(string="Cantidad")  # Cambiado a Integer para números enteros

    journal_id = fields.Many2one('account.journal', string='journal')

    def create(self, vals):
        record = super().create(vals)
        record.create_account_move(date=record.date, ref=record.receipt_number, amount=record.amount)
        # record.create_account_move(record.journal_id, record.document_type_id, record.date, record.receipt_number, record.amount)
        return record

    def create_account_move(self, journal_id=False, document_id=False, date=False, ref=False, amount=False, socio_id=False):
        # move_vals = {
        #     'move_type': 'entry',
        #     'date': date,
        #     'ref': ref,
        #     'render_account_id': self.request_id.id,
        #     'journal_id': journal_id.id,
        #     'l10n_latam_document_type_id': document_id.id,
        #     'l10n_latam_document_number': str(document_id.code) + str(self.id),
        #     'line_ids': [],
        # }
        # line_vals = [
        #     {
        #         'account_id': journal_id.default_account_id.id,
        #         'partner_id': socio_id,
        #         'debit': amount,
        #         'credit': 0.0,
        #         'name': 'Débito',
        #     },
        #     {
        #         #'account_id': cuenta_credito_id,
        #         'partner_id': socio_id,
        #         'debit': 0.0,
        #         'credit': amount,
        #         'name': 'Crédito',
        #     },
        # ]
        # move_vals['line_ids'] += [Command.create(vals) for vals in line_vals]
        # move_created = self.env['account.move'].create(move_vals)
        # move_created._post(soft=False)

        invoice = self.env['account.move'].create({
        'render_account_id': self.request_id.id,
        'move_type': 'in_invoice',
        'partner_id': self.partner_id.id,
        'invoice_date': date,
        'date': date,
        'l10n_latam_document_number': ref,
        'invoice_line_ids': [
            (0, 0, {
                'product_id': self.env.ref('ms_render_account_management.requests_payment_product_service').id,
                'price_unit': amount,
            }),
            ],
        })
        # invoice.action_post()
        return invoice


    @api.depends('unit_price', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = (line.unit_price or 0) * (line.unit_price or 0.0)


    @api.depends('unit_price', 'unit_price', 'has_additional_cost', 'additional_delivery_cost')
    def _compute_amount(self):
        for line in self:
            base = (line.unit_price or 0.0) * (line.unit_price or 0.0)
            extra = line.additional_delivery_cost if line.has_additional_cost else 0.0
            line.amount = base + extra