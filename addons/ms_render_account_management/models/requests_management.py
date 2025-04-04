from odoo import models, fields, api
import logging
from datetime import date

class MsRequestManagement(models.Model):
    _name = 'ms.request.management'
    _description = 'Modelo para gestinar las solicitudes'
    _inherit = 'mail.thread'

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
    # --------------------
    # fields
    # --------------------    
    name = fields.Char('name', compute="_compute_name")
    request_type = fields.Selection(TYPES_REQUEST, string='Request Type')
    project_id = fields.Many2one('account.analytic.account', string='project')
    activity_code = fields.Char('activity code')
    reference = fields.Char('Reference')
    rate = fields.Float('Rate', digits=(16, 3))
    date = fields.Date('Fecha', default=lambda self: date.today())
    voucher_number = fields.Char('Voucher number')
    amount = fields.Float('Amount', compute="_compute_amount")
    account_number = fields.Char('account number')
    account_number_detraction = fields.Char('account number detraction')
    status = fields.Selection(STATES, string='state', default="draft")

    general_objectives = fields.Text('general objectives')
    specific_objectives = fields.Text('specific objectives')
    address_service = fields.Text('address and service')
    person_profile = fields.Text('person profile')
    date_to = fields.Date('date to')
    date_of = fields.Date('date of')
    service_activities = fields.Text('service activities')
    accordance = fields.Text('accordance')
    
    # ---- DOCUMENTS FIELDS ----

    dni = fields.Binary('DNI')
    rh = fields.Binary('DJ (RH)')
    ruc_tab = fields.Binary('RUC tab')
    suspension = fields.Binary('Suspension')
    cv = fields.Binary('cv')
    power_validity = fields.Binary('Power validity')

    # --- DOCUEMENTS PAYEMENTS REQUESTS --
    format_eight = fields.Binary('Formato N°8')
    format_nine = fields.Binary('Formato N°9')
    # --------------------
    # relational fields
    # --------------------
    os_id = fields.Many2one('ms.request.management', string='os')
    partner_id = fields.Many2one('res.partner', string='partner', compute="_compute_partner", readonly=False, store=True)
    res_bank_id = fields.Many2one('res.bank', string='Bank')
    area_id = fields.Many2one('ms.account.system.settings', string='Area', domain="[('type', '=', 'areas')]")
    requests_lines_ids = fields.One2many('ms.requests.lines', 'request_id', string='requests lines')
    res_currency_id = fields.Many2one('res.currency', string='Currency',
                                      default=lambda self: self.env['res.currency'].search([('name', '=', 'PEN')], limit=1).id)
    
    service_id = fields.Many2one('ms.account.system.settings', string='service')
    payments_request_ids = fields.One2many('ms.payment.requests', 'request_id', string='payments')
    treasury_id = fields.Many2one('ms.treasury', string='Tesoreria')

    # dni = fields.Char('dni')  
    correlative = fields.Char('correlative')
    cost_center = fields.Char('cost center')
    dni_provider = fields.Char('dni provider')
    description_property = fields.Text('description property')
    tdr = fields.Char('TDR')
    responsible = fields.Char('responsible')

    account_move_ids = fields.One2many('account.move', 'render_account_id', string='account move')
    
    @api.depends('os_id')
    def _compute_partner(self):
        for record in self:
            if record.request_type == 'payment':
                if record.os_id and record.os_id.partner_id.id:
                    logging.info(record.os_id.partner_id)
                    logging.info('\n' * 5)

                    record.partner_id = record.os_id.partner_id
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

    @api.depends('requests_lines_ids')
    def _compute_amount(self):
        for request in self:
            request.amount = sum(line.amount for line in request.requests_lines_ids if line.amount)

    def action_valited_request(self):
        status = next(filter(lambda state: state[0] == self.status, self.STATES), None)
        if not status:
            self.status = 'draft'
            return
        index = 1 if self.STATES.index(status) == len(self.STATES) - 1 else self.STATES.index(status) + 1
        self.status = self.STATES[index][0]
    

    def decline_request(self):
        self.status = 'draft'

    @api.model
    def create(self, vals):
        record = super().create(vals)
        treasury_id = self.env['ms.treasury'].create({
            'project': record.project_id.name,
            'activity_code': record.activity_code,
            'reference' : record.reference,
            'rate': record.rate,
            'date': record.date,
            'voucher_number': record.voucher_number,
            'amount': record.amount,
            'account_number': record.account_number,
            'os_id': record.os_id.id,
            'partner_id': record.partner_id.id,
            'res_bank_id': record.res_bank_id.id,
            'area_id': record.area_id.id,
            'request_payment_id': record.id,
            'res_currency_id': record.res_currency_id.id
        })
        record.treasury_id = treasury_id.id
        return record
    

    @api.onchange('os_id')
    def _onchange_os_id(self):
        if self.os_id:
            self.project_id = self.os_id.project_id
        else:
            self.project_id = False