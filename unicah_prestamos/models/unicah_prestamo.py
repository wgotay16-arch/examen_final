from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UnicahPrestamo(models.Model):
    _name = "unicah.prestamo"
    _description = "Préstamo de equipo universitario"
    _order = "fecha_inicio desc"

    name = fields.Char(
        string="Equipo",
        required=True,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Solicitante",
        required=True,
    )

    fecha_inicio = fields.Date(
        string="Fecha de préstamo",
        required=True,
        default=fields.Date.context_today,
    )

    fecha_devolucion = fields.Date(
        string="Fecha de devolución",
        required=True,
    )

    estado = fields.Selection(
        [
            ("prestado", "Prestado"),
            ("devuelto", "Devuelto"),
        ],
        string="Estado",
        default="prestado",
        required=True,
    )

    observaciones = fields.Text(
        string="Observaciones",
    )

    dias_prestamo = fields.Integer(
        string="Días de préstamo",
        compute="_compute_dias_prestamo",
        store=True,
    )

    @api.depends("fecha_inicio", "fecha_devolucion")
    def _compute_dias_prestamo(self):
        for prestamo in self:
            if prestamo.fecha_inicio and prestamo.fecha_devolucion:
                prestamo.dias_prestamo = (
                    prestamo.fecha_devolucion - prestamo.fecha_inicio
                ).days
            else:
                prestamo.dias_prestamo = 0

    @api.constrains("fecha_inicio", "fecha_devolucion")
    def _check_fechas(self):
        for prestamo in self:
            if (
                prestamo.fecha_inicio
                and prestamo.fecha_devolucion
                and prestamo.fecha_devolucion < prestamo.fecha_inicio
            ):
                raise ValidationError(
                    "La fecha de devolución no puede ser anterior "
                    "a la fecha de préstamo."
                )
