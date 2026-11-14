from odoo import api, fields, models
from odoo.exceptions import UserError

LIMITE_UNIDADES_ESTUDIANTE = 10



class SaleOrder(models.Model):
    _inherit = "sale.order"

    tipo_cliente = fields.Selection(
        related="partner_id.tipo_cliente",
        string="Tipo de cliente"
    )

    convenio_id = fields.Many2one(
        "tienda.convenio",
        string="Convenio",
        compute="_compute_convenio_id",
        store=True,
        readonly=False,
        domain="[('tipo_cliente', '=', tipo_cliente)]",
    )

    convenio_aplicado = fields.Boolean(
        string="Convenio aplicado",
        readonly=True,
        copy=False
    )


    def action_confirm(self):
        for order in self:
            if order.tipo_cliente == "estudiante":

                total_unidades = sum(
                    line.product_uom_qty
                    for line in order.order_line
                    if not line.display_type
                )

                if total_unidades > LIMITE_UNIDADES_ESTUDIANTE:
                    raise UserError(
                        f"Los estudiantes tienen un límite de "
                        f"{LIMITE_UNIDADES_ESTUDIANTE} unidades "
                        f"por pedido. Este pedido contiene "
                        f"{total_unidades:g} unidades."
                    )

        return super().action_confirm()


    @api.depends("partner_id", "date_order")
    def _compute_convenio_id(self):
        for order in self:
            fecha = (
                order.date_order or fields.Datetime.now()
            ).date()

            order.convenio_id = self.env[
                "tienda.convenio"
            ].search([
                ("tipo_cliente", "=", order.partner_id.tipo_cliente),
                ("fecha_inicio", "<=", fecha),
                "|",
                ("fecha_fin", "=", False),
                ("fecha_fin", ">=", fecha),
            ], limit=1)

    def action_aplicar_convenio(self):
        for order in self:
            if order.state not in ("draft", "sent"):
                raise UserError(
                    "Solo se puede aplicar un convenio a una cotización."
                )

            if not order.convenio_id:
                raise UserError(
                    "El pedido no tiene un convenio asignado."
                )

            lineas = order.order_line.filtered(
                lambda line: not line.display_type
            )

            lineas.write({
                "discount": order.convenio_id.porcentaje
            })

            order.convenio_aplicado = True

            order.message_post(
                body=f"Se aplicó el {order.convenio_id.name} "
                     f"con {order.convenio_id.porcentaje:g} % de descuento."
            )
