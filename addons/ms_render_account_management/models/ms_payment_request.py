from odoo import models, fields, api


class MsPaymentRequest(models.Model):
    _name = 'ms.payment.requests'
    _description = 'Pagos de solicitudes/Documentos'
    
    receipt_number = fields.Char('receipt number')
    date = fields.Date('date')
    details = fields.Text('details')
    amount = fields.Float('amount')
    request_id = fields.Many2one('ms.request.management', string='request')
    partner_id = fields.Many2one('res.partner', string='Proveedor')  # Campo de proveedor

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Después, se crea la factura usando el método _create_account_move
        record._create_account_move()
        return record

    def _create_account_move(self):
        product = self.env.ref('ms_render_account_management.requests_payment_product_service', raise_if_not_found=False)
        if not product:
            raise ValueError("No se encontró el producto 'requests_payment_product_service'.")
        
        move_vals = {
            'move_type': 'in_invoice',  # Tipo de factura (Factura de proveedor)
            'partner_id': self.partner_id.id,  # Proveedor
            'invoice_date': self.date,  # Fecha de la factura
            'date': self.date,  # Fecha contable
            'l10n_latam_document_number': self.receipt_number,  # Número de documento
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': product.id,  # Producto relacionado con el pago
                    'price_unit': self.amount,  # Importe del pago
                    'quantity': 1,  # Cantidad
                    'name': self.details,  # Detalles del pago
                }),
            ],
        }

        # Crear la factura
        move = self.env['account.move'].create(move_vals)
        return move
