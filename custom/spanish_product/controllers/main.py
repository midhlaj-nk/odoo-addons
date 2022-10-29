from odoo import http
from odoo.http import request


class elearning(http.Controller):

    @http.route('/#####', type="json", auth="public", website=True)
    def onchange(self, **kw):
        print("set")