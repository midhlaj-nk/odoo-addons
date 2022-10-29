# from odoo.http import route, request
# from odoo import http
# from odoo.addons.website_sale.controllers.main import WebsiteSale
#
#
# class WebsiteSiteInherit(WebsiteSale):
#     @http.route('/shop', type='http', auth="public", website=True)
#     def shop(self, **post):
#         res = super(WebsiteSiteInherit, self).shop()
#         i = res.qcontext
#         product_id = i['products']
#         for p in (product_id):
#             print(p.qty_available)
#         print(p)
#
#         # for i in res.qcontext:
#         #     names = i['products']
#
#         return res
