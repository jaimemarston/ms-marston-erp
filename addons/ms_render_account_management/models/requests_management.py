from odoo import models, fields, api


class MsRequestManagement(models.Model):
    _name = 'ms.request.management'
    _description = 'Modelo para gestinar las solicitudes'

    
    # --------------------
    # fields
    # --------------------    
    name = fields.Char('name', compute="_compute_name")
    request_type = fields.Selection([
        ('payment', 'Payment'),
        ('render', 'to Render'),
        ('surrenders', 'Surrenders'),
        ('contract', 'Contract'),
        ('refund', 'Refund')
    ], string='Request Type')
    project = fields.Char('project')
    activity_code = fields.Char('activity code')
    reference = fields.Char('Reference')
    rate = fields.Float('Rate', digits=(16, 3))
    date = fields.Date('Date')
    voucher_number = fields.Char('Voucher number')
    amount = fields.Float('Amount', compute="_compute_amount", digits=(16, 3))

    # --------------------
    # relational fields
    # --------------------
    partner_id = fields.Many2one('res.partner', string='partner')
    res_bank_id = fields.Many2one('res.bank', string='Bank')
    area_id = fields.Many2one('ms.request.settings', string='Area', domain="[('type', '=', 'areas')]")
    requests_lines_ids = fields.One2many('ms.requests.lines', 'request_id', string='requests lines')
    res_currency_id = fields.Many2one('res.currency', string='Currency')
    account_number = fields.Char('account number')
    account_number_detraction = fields.Char('account number detraction')

    
    dni = fields.Char('dni')  
    correlative = fields.Char('correlative')
    cost_center = fields.Char('cost center')
    dni_provider = fields.Char('dni provider')
    description_property = fields.Text('description property')
    tdr = fields.Char('TDR')
    responsible = fields.Char('responsible')

    account_move_ids_ids = fields.One2many('account.move', 'render_account_id', string='account move')

    @api.depends('area_id', 'activity_code')
    def _compute_name(self):
        for request in self:
            name = "#"
            if request.area_id:
                name = name + "-" + request.area_id.name
            if request.activity_code:
                name = name + "-" + request.activity_code
            request.name = name

    @api.depends('requests_lines_ids')
    def _compute_amount(self):
        for request in self:
            request.amount = sum(line.amount for line in request.requests_lines_ids if line.amount)
            