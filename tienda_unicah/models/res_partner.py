from odoo import api, fields, models
from odoo.exceptions import ValidationError



TIPOS_CLIENTE = [
    ("estudiante", "Estudiante"),
    ("docente", "Docente"),
    ("administrativo", "Administrativo"),
    ("externo", "Externo"),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    tipo_cliente = fields.Selection(
        selection=TIPOS_CLIENTE,
        string="Tipo de cliente",
        default="externo",
    )

    numero_cuenta = fields.Char(
        string="Número de cuenta",
        copy=False,
    )

    carrera = fields.Char(
        string="Carrera",
    )
    
    @api.constrains("tipo_cliente", "numero_cuenta")
    def _check_numero_cuenta(self):
        for partner in self:
            if partner.tipo_cliente == "estudiante":
                numero = partner.numero_cuenta or ""

                if len(numero) != 10 or not (
                    numero.isascii() and numero.isdecimal()
                ):
                    raise ValidationError(
                        "El número de cuenta del estudiante "
                        "debe contener exactamente 10 dígitos numéricos."
                    )


