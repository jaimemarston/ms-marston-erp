from odoo import models, fields
import logging
class AccountMove(models.Model):
    _inherit = "account.move"
    

    render_account_id = fields.Many2one('ms.request.management', string='render account')

    def action_tenders_payment_invoice(self):
        if self.payment_state != "paid":
            self.sudo().write({
                'payment_state': 'paid'
            })
            return True
