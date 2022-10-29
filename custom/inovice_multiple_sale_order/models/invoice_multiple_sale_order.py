from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'account.move'
    sale_order_ids = fields.Many2many('sale.order',
                                      domain="[('invoice_status','=','to invoice')]")

    @api.onchange('sale_order_ids')
    def addlines(self):
        self.invoice_line_ids = False
        self.line_ids = False
        print('this invoice linee ids',self.invoice_line_ids)
        for i in self.sale_order_ids.order_line:

            self.invoice_line_ids = [(0, 0, {
                'product_id': i.product_id,
                'price_unit': i.price_unit,
                'quantity' : i.product_uom_qty,
                'tax_ids' : i.tax_id,
                'currency_id': self.company_id.currency_id,

            })]
            self._move_autocomplete_invoice_lines_values()

    def action_post(self):
        super(SaleOrderLine, self).action_post()
        # print('super')
        for i in self.sale_order_ids.order_line:
            print(i)
            i.qty_invoiced=i.product_uom_qty
            i.invoice_status = 'invoiced'

