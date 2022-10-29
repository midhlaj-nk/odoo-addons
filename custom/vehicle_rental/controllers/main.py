import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name,
                        token='rty', **kw):
        uid = request.session.uid
        report_obj = request.env[model].sudo(uid)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'), (
                        'Content-Disposition',
                        content_disposition(report_name + '.xlsx'))
                             ]
                )
                report_obj.get_xlsx_report(options, response)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))


class RentalRequests(http.Controller):

    @http.route('/rental_request', auth='public', website=True)
    def request_webform(self):
        customer_rec = request.env['res.partner'].sudo().search([])
        vehicle_rec = request.env['rental.vehicle'].sudo().search([])

        period_rec = request.env['rent.charges'].sudo().search([])
        # print(vehicle_rec)
        return request.render('vehicle_rental.rental_request',
                              {'customer_rec': customer_rec,
                               'vehicle_rec': vehicle_rec,
                               'period_rec': period_rec},
                              )

    @http.route('/onchange', type="json", auth="public", website=True)
    def onchange(self, **kw):
        vehicle = (kw.get('vehicle'))
        period_rec = request.env['rent.charges'].sudo().search(
            [('vehicle_id', '=', int(vehicle))])
        # print(period_rec, 'search values')
        list=[]
        for i in period_rec:
            dic = {'id': i.id,'ptype':i.period_type}
            list.append(dic)
            print(dic)
        print(list)
        return list

    @http.route('/create/webrequest', type="http", auth="public", website=True)
    def create_webrequest(self, **kw):
        print(kw)
        req_val = {
            'customer': kw.get('customer_name'),
            'vehicle_id': kw.get('vehicle'),
            'from_date': kw.get('from_date'),
            'to_date': kw.get('to_date'),
            'period_type':int(kw.get('period_type')),
        }
        print(req_val)
        request.env['rental.request'].sudo().create(req_val)
        return request.render('website.contactus_thanks', {})
