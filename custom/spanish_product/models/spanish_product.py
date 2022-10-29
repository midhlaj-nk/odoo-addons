from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SpanishProduct(models.Model):
    _inherit = 'product.product'

    spanish_product = fields.Char()
