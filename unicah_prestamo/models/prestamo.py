from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UnicahPrestamo(models.Model):
    _name = "unicah.prestamo"
    _description = "Préstamo de equipo"

    name = fields.Char(string="Equipo", required=True)
    partner_id = fields.Many2one("res.partner", string="Solicitante", required=True)
    fecha_prestamo = fields.Date(
        string="Fecha de préstamo", required=True, default=fields.Date.context_today
    )
    fecha_limite = fields.Date(string="Fecha límite", required=True)
    state = fields.Selection(
        [("prestado", "Prestado"), ("devuelto", "Devuelto")],
        string="Estado",
        default="prestado",
    )
    dias_prestamo = fields.Integer(string="Días de préstamo", compute="_compute_dias")

    @api.depends("fecha_prestamo", "fecha_limite")
    def _compute_dias(self):
        for p in self:
            if p.fecha_prestamo and p.fecha_limite:
                p.dias_prestamo = (p.fecha_limite - p.fecha_prestamo).days
            else:
                p.dias_prestamo = 0

    @api.constrains("fecha_prestamo", "fecha_limite")
    def _check_fechas(self):
        for p in self:
            if p.fecha_limite < p.fecha_prestamo:
                raise ValidationError(
                    "La fecha límite no puede ser anterior a la fecha de préstamo."
                )

    def action_devolver(self):
        self.write({"state": "devuelto"})
