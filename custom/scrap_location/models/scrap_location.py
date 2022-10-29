from odoo import fields, models, api
from odoo.exceptions import ValidationError


class scrap(models.Model):
    _inherit = 'stock.scrap'

    @api.onchange('product_id')
    def product_change(self):
        records= self.env['stock.putaway.rule'].search([('product_id.id', '=', self.product_id.id)])
        self.location_id = records.location_out_id.id

    def action_validate(self):
        raise ValidationError(
            'The source location is not correct.')




