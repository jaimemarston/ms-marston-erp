from odoo import models, fields, api

class TravelRequest(models.Model):
    _name = 'travel.request'
    _description = 'Travel Request Form'
    _inherit = ['mail.thread']

    # Campos básicos
    name = fields.Char(string='Referencia', readonly=True, default='Nuevo')
    STATES = [
        ('draft', 'V°B° Solicitante'),
        ('stage_1', 'V°B° Jefatura'),
        ('stage_2', 'V°B° Direccion'),
        ('stage_3', 'V°B° Contable'),
        ('stage_4', 'V°B° Logistica'),
        ('stage_5', 'Contabilidad'),
        ('cancelled', 'Anulado'),
    ]

    status = fields.Selection(STATES, string='state', default="draft")

    # Información general
    employee_id = fields.Many2one(
    'hr.employee', 
    string='Empleado',
    required=False,  # Cambiar a False si no es obligatorio
    )

    dni = fields.Char(related='employee_id.identification_id', string='DNI', readonly=False)
    phone = fields.Char(related='employee_id.mobile_phone', string='Teléfono', readonly=False)
    birth_date = fields.Date(related='employee_id.birthday', string='Fecha Nacimiento', readonly=False)
    
    project_id = fields.Many2one('account.analytic.account', string='Proyecto')
    area_responsible_id = fields.Many2one('hr.employee', string='Responsable de Área')
    administrator_id = fields.Many2one('hr.employee', string='Administrador')
    
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
    total_amount = fields.Float(string='Total', compute='_compute_total_amount', store=True, digits=(12, 2))


    @api.onchange('transport_air')
    def _onchange_transport_air(self):
        if self.transport_air:
            self.transport_land = False

    @api.onchange('transport_land')
    def _onchange_transport_land(self):
        if self.transport_land:
            self.transport_air = False


    @api.depends('activity_type_ids.amount')  # Depende de los campos 'amount' de las actividades
    def _compute_total_amount(self):
        for rec in self:
            # Sumamos el monto de todas las actividades relacionadas
            rec.total_amount = sum(activity.amount for activity in rec.activity_type_ids)


    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('travel.request') or 'Nuevo'
        return super().create(vals)
    

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