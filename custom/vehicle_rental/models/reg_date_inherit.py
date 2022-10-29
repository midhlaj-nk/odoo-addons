from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    reg_date1 = fields.Date(string="Registration Date")

