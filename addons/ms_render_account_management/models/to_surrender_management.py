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
        ('stage_5', 'V°B Tesoreria'),
    ]

    name = fields.Char('name', compute="_compute_name")
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
    def _compute_name(self):
        for record in self:
            name = ""
            if record.request_type in ['contract', 'os', 'oc']:
                name = ("C-" if record.request_type == "contract" else "OS-" if record.request_type == 'os' else "OC-") + str(record.id)
            else:
                name = "#"
                if record.area_id:
                    name = name + "-" + record.area_id.name
                if record.activity_code:
                    name = name + "-" + record.activity_code
            record.name = name


    def action_valited_request(self):
        status = next(filter(lambda state: state[0] == self.status, self.STATES), None)
        if not status:
            self.status = 'draft'
            return
        index = 1 if self.STATES.index(status) == len(self.STATES) - 1 else self.STATES.index(status) + 1
        self.status = self.STATES[index][0]
    
    def decline_request(self):
        self.status = 'draft'