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
        ('sp', 'S.P'),
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
    # --------------------
    # fields
    # --------------------    
    justification= fields.Text(string="Justificacion de Eleccion de Proveedor")
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
    # Campo computado para visualización HTML
    status_html = fields.Html(
        string='Estado Visual',
        compute='_compute_status_html',
        store=True
    )
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
    proposal_one = fields.Binary('proposal one')
    proposal_two = fields.Binary('proposal two')
    quotation_file_1 = fields.Binary('Cotización 1')
    quotation_file_2 = fields.Binary('Cotización 2')
    quotation_file_3 = fields.Binary('Cotización 3')

    # --- DOCUEMENTS PAYEMENTS REQUESTS --
    format_eight = fields.Binary('Formato N°8')
    format_nine = fields.Binary('Formato N°9')
    format_two = fields.Binary('Formato N°2')

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

    to_render_id = fields.Many2one('to.surrender.management', string="Documento")

    # dni = fields.Char('dni')  
    correlative = fields.Char('correlative')
    cost_center = fields.Char('cost center')
    dni_provider = fields.Char('dni provider')
    description_property = fields.Text('description property')
    tdr = fields.Char('TDR')
    responsible = fields.Char('responsible')

    account_move_ids = fields.One2many('account.move', 'render_account_id', string='account move')
    
     # Relaciones a los formatos 8 y 9
    activity_report_ids = fields.One2many('ms.activity.report','request_id',string='Informes de Actividad')
    conformity_report_ids = fields.One2many('ms.conformity.report','request_id',string='Actas de Conformidad')



# ------------------------------------fields de travel----------------------------------------

    dni_ident = fields.Char(string='DNI', readonly=False)
    phone = fields.Char(string='Teléfono', readonly=False)
    birth_date = fields.Date(string='Fecha Nacimiento', readonly=False)
    reason = fields.Text(string='Motivo del Viaje')
    departure_date = fields.Date(string='Fecha de Salida')
    return_date = fields.Date(string='Fecha de Retorno')

    # Capacitación
    training_type = fields.Selection([
        ('teachers', 'Capacitación docentes'),
        ('directors', 'Capacitación directivos'),
        ('other', 'Otro')
    ], string='Tipo de Capacitación')

    # Transporte
    transport_air = fields.Boolean(string='Transporte Aéreo')
    transport_land = fields.Boolean(string='Transporte Terrestre')

    # Presupuesto
    activity_type_ids = fields.One2many('travel.activity', 'request_id', string='Actividades')
    

    @api.onchange('transport_air')
    def _onchange_transport_air(self):
        if self.transport_air:
            self.transport_land = False

    @api.onchange('transport_land')
    def _onchange_transport_land(self):
        if self.transport_land:
            self.transport_air = False



    
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
            if record.request_type in ['contract', 'os', 'oc', 'sp']:
                name = ("C-" if record.request_type == "contract" 
                        else "OS-" if record.request_type == 'os' 
                        else "OC-" if record.request_type == 'oc' 
                        else "SP-") + str(record.id)
            else:
                name = "#"
                if record.area_id:
                    name = name + "-" + record.area_id.name
                if record.activity_code:
                    name = name + "-" + record.activity_code
            record.name = name


    @api.depends('requests_lines_ids.amount', 'payments_request_ids.amount', 'activity_type_ids.amount')
    def _compute_amount(self):
        for record in self:
            lines_total = sum(line.amount for line in record.requests_lines_ids)
            payments_total = sum(record.payments_request_ids.mapped('amount'))
            record.amount = lines_total + payments_total


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
            self.area_id = self.os_id.area_id
            self.activity_code = self.os_id.activity_code
        else:
            self.project_id = False


    @api.depends('status')
    def _compute_status_html(self):
        state_classes = {
            'draft': 'text-bg-warning',
            'stage_1': 'text-bg-info',
            'stage_2': 'text-bg-primary',
            'stage_3': 'text-bg-secondary',
            'stage_4': 'text-bg-dark',
            'stage_5': 'text-bg-success',
            'cancelled': 'text-bg-danger',
        }
        
        for record in self:
            if record.status:
                display_value = dict(self.STATES).get(record.status)
                record.status_html = f'''
                    <span class="badge rounded-pill {state_classes.get(record.status, 'text-bg-light')}">
                        {display_value}
                    </span>
                '''
            else:
                record.status_html = ''
    
    def action_cancel_request(self):
        for rec in self:
            rec.status = 'cancelled'
