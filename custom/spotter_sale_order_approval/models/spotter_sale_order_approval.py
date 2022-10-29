from odoo import fields, models


class SpotterSaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
        ('approval1', 'Approval1'),
        ('approval2', 'Approval2'),
    ], )

    def action_approval1(self):
        self.state = 'approval2'

    def action_approval2(self):
        self.state = 'sale'

    def action_confirm(self):
        if self.amount_total > 2500:
            self.state = 'approval1'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': "The sale has been sent for approval",
                    'type': 'rainbow_man',
                }
            }
        else:
            super(SpotterSaleOrder, self).action_confirm()

