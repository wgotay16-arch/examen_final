from odoo import api, fields, models
from odoo.exceptions import ValidationError

from .res_partner import TIPOS_CLIENTE



class TiendaConvenio(models.Model):
    _name = "tienda.convenio"
    _description = "Convenio de descuento"

    name = fields.Char(string="Nombre", required=True)

    tipo_cliente = fields.Selection(
        TIPOS_CLIENTE,
        string="Tipo de cliente",
        required=True
    )

    porcentaje = fields.Float(
        string="Descuento (%)",
        required=True
    )

    fecha_inicio = fields.Date(
        string="Desde",
        required=True,
        default=fields.Date.context_today
    )

    fecha_fin = fields.Date(string="Hasta")

    active = fields.Boolean(
        string="Activo",
        default=True
    )


    @api.constrains("porcentaje", "fecha_inicio", "fecha_fin")
    def _check_convenio(self):
        for convenio in self:

            if convenio.porcentaje <= 0 or convenio.porcentaje > 40:
                raise ValidationError(
                    "El porcentaje de descuento debe ser "
                    "mayor que 0 y no superar el 40 %."
                )

            if (
                convenio.fecha_fin
                and convenio.fecha_inicio
                and convenio.fecha_fin < convenio.fecha_inicio
            ):
                raise ValidationError(
                    "La fecha final del convenio no puede "
                    "ser anterior a la fecha inicial."
                )

