from odoo import models, api, fields
import json


class CustomerInvoice(models.Model):
    _inherit = "account.move"

    def get_widget_customer_invoice(self):
        content = self.invoice_payments_widget["content"]
        if content:
            return content
        return
