from odoo import fields, models, api


class DeliveryRoute(models.Model):
    _name = "delivery.route"
    _description = "Customer Route Management"
    _rec_name = 'location'

    location = fields.Char()
    delivery_location_ids = fields.One2many('delivery.route.location',
                                            'routes_id')


class Routes(models.Model):
    _name = "delivery.route.location"
    _description = "routes of delivery"
    _rec_name = 'routes'

    routes_id = fields.Many2one('delivery.route', 'location')
    routes = fields.Char()
    customer_details = fields.Many2many('res.partner',routes_id, compute='_filter_customer')

    @api.depends('routes')
    def _filter_customer(self):
        self.customer_details = self.env['res.partner'].search(
            [('routes_inherit_id', '=', self.id)])


class InheritRespartner(models.Model):
    _inherit = 'res.partner'

    routes_inherit_id = fields.Many2one('delivery.route.location', 'routes')


