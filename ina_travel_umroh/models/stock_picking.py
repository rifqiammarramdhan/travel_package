from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        picking = super(StockPicking, self).create(vals)
        for move in picking.move_ids:
            sale_order_line = self.env["sale.order.line"].search(
                [
                    ("order_id", "=", picking.sale_id.id),
                    ("product_id", "=", move.product_id.id),
                ],
                limit=1,
            )
            if sale_order_line:
                move.product_uom_qty = sale_order_line.product_uom_qty
        return picking

    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        for picking in self:
            for move in picking.move_ids:
                sale_order_line = self.env["sale.order.line"].search(
                    [
                        ("order_id", "=", picking.sale_id.id),
                        ("product_id", "=", move.product_id.id),
                    ],
                    limit=1,
                )
                if sale_order_line:
                    move.product_uom_qty = sale_order_line.product_uom_qty
        return res

    def action_print_delivery(self):
        return self.env.ref(
            "ina_travel_umroh.report_delivery_order_action"
        ).report_action(self)
