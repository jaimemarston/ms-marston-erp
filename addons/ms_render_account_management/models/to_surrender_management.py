from odoo import models, fields, api
import logging
from datetime import date

class ToSurrenderManagement(models.Model):
    _name = 'to.surrender.management'
    _description = 'Modelo para rendir'
    _inherit = 'mail.thread'

    # fields declaration
    # --------------------------------------------------------------------------------------------------

    TYPES_REQUEST = [
        ('payment', 'Payment'),
        ('render', 'to Render'),
        ('surrenders', 'Surrenders'),
        ('contract', 'Contract'),
        ('refund', 'Refund'),
        ('os', 'O.S'),
        ('oc', 'O.C'),
    ]

    STATES = [
        ('draft', 'V°B° Solicitante'),
        ('stage_1', 'V°B° Jefatura'),
        ('stage_2', 'V°B° Direccion'),
        ('stage_3', 'V°B° Contable'),
        ('stage_4', 'V°B° Logistica'),
        ('stage_5', 'Contabilidad'),
        ('cancelled', 'Anulado'),
    ]

    name = fields.Char('name', compute="_compute_name_to")
    partner_id = fields.Many2one('res.partner', string='partner', compute="_compute_partner", readonly=False, store=True)
    area_id = fields.Many2one('ms.account.system.settings', string='Area', domain="[('type', '=', 'areas')]")
    project_id = fields.Many2one('account.analytic.account', string='project')
    activity_code = fields.Char('activity code')
    reference = fields.Char('Reference')
    res_bank_id = fields.Many2one('res.bank', string='Bank')
    account_number = fields.Char('account number')
    account_number_detraction = fields.Char('account number detraction')
    res_currency_id = fields.Many2one('res.currency', string='Currency',
                                      default=lambda self: self.env['res.currency'].search([('name', '=', 'PEN')], limit=1).id)

    date = fields.Date('Fecha', default=lambda self: date.today())
    service_id = fields.Many2one('ms.account.system.settings', string='service', domain="[('type', '=', 'service')]")
    amount = fields.Float('Amount')
    correlative = fields.Char('correlative')
    os_id = fields.Many2one('ms.request.management', string='os')
    request_type = fields.Selection(TYPES_REQUEST, string='Request Type')
    status = fields.Selection(STATES, string='state', default="draft")






    # Methods
    # --------------------------------------------------------------------------------------------------
    @api.depends('os_id')
    def _compute_partner(self):
        for record in self:
            if record.request_type == 'payment':
                if record.os_id and record.os_id.partner_id.id:
                    logging.info(record.os_id.partner_id)
                    logging.info('\n' * 5)


    @api.depends('area_id', 'activity_code')
    def _compute_name_to(self):
        for record in self:
            # Si 'request_type' es 'surrenders', asignar "AR-" seguido del id
            if not record.request_type:
                record.name = "AR-" + str(record.id)


    def action_valited_request(self):
        for record in self:
            # Evitar avanzar si el estado es 'cancelled'
            if record.status == 'cancelled':
                continue
            # Crear secuencia de estados que NO incluye 'cancelled'
            valid_states = [s[0] for s in record.STATES if s[0] != 'cancelled']
            # Obtener índice actual del estado
            if record.status not in valid_states:
                record.status = 'draft'
                continue
            current_index = valid_states.index(record.status)
            # Solo avanzar si no estamos en el último estado
            if current_index < len(valid_states) - 1:
                record.status = valid_states[current_index + 1]

    def decline_request(self):
        self.status = 'draft'