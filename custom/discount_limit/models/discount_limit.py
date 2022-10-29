from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DiscountLimit(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_limit = fields.Integer(string="Discount Limit")

    def set_values(self):
        super(DiscountLimit, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'Discount_limit.discount_limit', self.discount_limit)

    def get_values(self):
        res = super(DiscountLimit, self).get_values()
        res['discount_limit'] = self.env[
            'ir.config_parameter'].sudo().get_param(
            'Discount_limit.discount_limit')
        print(res['discount_limit'])
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def get_values(self):
        # print('order date', self.date_order)
        from_date = fields.Datetime.today().replace(day=1)
        date_inc = from_date.month + 1
        to_date = from_date.replace(month=date_inc)
        # print('to_date', to_date)
        records = self.env['sale.order'].search(
            ['&', '&', ('state', '=', 'sale'),
             ('date_order', '>=', from_date),
             ('date_order', '<', to_date)])

        total_disc = 0
        for rec in records:
            for val in rec.order_line:
                total_price = val.price_unit * val.product_uom_qty
                discounted_amount = (total_price / 100) * val.discount
                total_disc = total_disc + discounted_amount

        print(total_disc)

        params = self.env['ir.config_parameter'].sudo()
        discount_limit = params.get_param('Discount_limit.discount_limit')

        for rec in self:
            for val in rec.order_line:
                if total_disc >= float(
                        discount_limit) and val.discount != False:
                    raise ValidationError(
                        'Monthly limit has been exceeded')

