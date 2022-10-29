from odoo import http
from odoo.http import request


class StockAvailability(http.Controller):

    @http.route('/shop', type="json", auth="public", website=True)
    def stock_availability(self, **kw):
        course = request.env['product.product'].sudo().search([])

        return list
