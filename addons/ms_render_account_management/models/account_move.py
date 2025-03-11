from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"
    

    render_account_id = fields.Many2one('ms.request.management', string='render account')