from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DiscountPosCustom(models.Model):
    _inherit = 'pos.config'

    discount_pos_cust = fields.Selection(
        [('percentage', 'Percentage'), ('amount', 'Amount')], required=True,
        index=True, string="Discount on POS")
