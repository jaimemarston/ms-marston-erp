from odoo import models, fields, api
import logging

class MsTreasury(models.Model):
    _name = 'ms.treasury'
    _description = 'Modelo de tesoreria para solicitudes de pagos'
    

    project = fields.Char('project')
    activity_code = fields.Char('activity code')
    reference = fields.Char('Reference')
    rate = fields.Float('Rate', digits=(16, 3))
    date = fields.Date('Date')
    voucher_number = fields.Char('Voucher number')
    amount = fields.Float('Monto')
    account_number = fields.Char('account number')
    account_number_detraction = fields.Char('account number detraction')
    os_id = fields.Many2one('ms.request.management', string='os')
    partner_id = fields.Many2one('res.partner', string='partner')
    res_bank_id = fields.Many2one('res.bank', string='Bank')
    area_id = fields.Many2one('ms.request.settings', string='Area', domain="[('type', '=', 'areas')]")
    request_payment_id = fields.Many2one('ms.request.management', string='Solicitud de pago')
    res_currency_id = fields.Many2one('res.currency', string='Currency')
    status = fields.Selection([
        ('pending', 'Pendiente de pago'),
        ('paid', 'Pagado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='pending')
        # Este es el campo que contendrá el HTML para el estado
    status_html = fields.Html(string='Estado HTML', compute='_compute_status_html')

    @api.depends('status')
    def _compute_status_html(self):
        for record in self:
            if record.status == 'pending':
                record.status_html = '<span class="badge rounded-pill text-bg-warning">Pendiente de pago</span>'
            elif record.status == 'paid':
                record.status_html = '<span class="badge rounded-pill text-bg-success">Pagado</span>'
            elif record.status == 'cancelled':
                record.status_html = '<span class="badge rounded-pill text-bg-danger">Cancelado</span>'
            else:
                record.status_html = ''