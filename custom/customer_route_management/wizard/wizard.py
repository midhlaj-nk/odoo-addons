import json
import io
from odoo import fields, models
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class RouteReportWizard(models.TransientModel):
    _name = 'route.report.wizard'
    _description = 'Reporting wizard'

    routes_wizard = fields.Many2many('delivery.route')
    show_due_amount = fields.Boolean()
    total_due_only = fields.Boolean()

    def print_pdf(self):
        location_val = tuple(self.routes_wizard.mapped('id'))
        routes_val = []
        for rec in self.env['delivery.route.location'].search([]):
            routes_val.append(rec.routes)

        location = []
        for rec in self.routes_wizard:
            location.append(rec.location)

        if self.show_due_amount == True:
            print("show_due_amount is truee>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            qy = ("""select res_partner.name as customer,
                            res_partner.id as cus_id,
                            delivery_route_location.routes as route,
                            res_partner.phone as phone,
                            res_partner.street as street,
                            res_partner.street2 as street2,
                            res_partner.city as city,
                            res_country_state.name as state,
                            res_partner.zip as zip,
                            res_country.name as country,
                            res_partner.email as email,
                            delivery_route.location as locname,
                            delivery_route.id as locid,
                            account_move.amount_total as amt,
							account_move.payment_reference as invoice,
							account_move.payment_state,
							account_move.invoice_date_due as inv_date




                                                        FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
            														 JOIN res_country_state on res_partner.state_id = res_country_state.id
            														 JOIN res_country on res_partner.country_id = res_country.id
            														 JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
            														 LEFT JOIN account_move on res_partner.id = account_move.partner_id


                                                                                  where delivery_route.id in {} """.format(
                tuple(self.routes_wizard.ids)))

            if len(tuple(self.routes_wizard.ids)) == 1:
                qy = ("""select res_partner.name as customer,
                                            res_partner.id as cus_id,
                                            delivery_route_location.routes as route,
                                            res_partner.phone as phone,
                                            res_partner.street as street,
                                            res_partner.street2 as street2,
                                            res_partner.city as city,
                                            res_country_state.name as state,
                                            res_partner.zip as zip,
                                            res_country.name as country,
                                            res_partner.email as email,
                                            delivery_route.location as locname,
                                            delivery_route.id as locid,
                                            account_move.amount_total as amt,
                							account_move.payment_reference as invoice,
                							account_move.payment_state,
                							account_move.invoice_date_due as inv_date




                                                                        FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
                            														 JOIN res_country_state on res_partner.state_id = res_country_state.id
                            														 JOIN res_country on res_partner.country_id = res_country.id
                            														 JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
                            														 LEFT JOIN account_move on res_partner.id = account_move.partner_id


                                                                                                 where delivery_route.id = '%s'  """ % (
                    location_val
                ))
            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(qdata)
            print("uuuu", qdata)


            data_length = len(qdata)

            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'location': location,
                'routes': routes_val,
                'd_length': data_length
            }
            # print(data)
            return \
                self.env.ref(
                    'customer_route_management.route_report_action').report_action(
                    self,
                    data=data)

        else:
            qy = ("""select res_partner.name as customer,
                res_partner.id as cus_id,
                delivery_route_location.routes as route,
                res_partner.phone as phone,
                res_partner.street as street,
                res_partner.street2 as street2,
                res_partner.city as city,
                res_country_state.name as state,
                res_partner.zip as zip,
                res_country.name as country,
                res_partner.email as email,
                delivery_route.location as locname,
                delivery_route.id as locid

                                            FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
														 JOIN res_country_state on res_partner.state_id = res_country_state.id
														 JOIN res_country on res_partner.country_id = res_country.id
														 JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
                                                                      where delivery_route.id in {} """.format(
                tuple(self.routes_wizard.ids)))
            if len(tuple(self.routes_wizard.ids)) == 1:
                qy = ("""select res_partner.name as customer,
                                res_partner.id as cus_id,
                                delivery_route_location.routes as route,
                                res_partner.phone as phone,
                                res_partner.street as street,
                                res_partner.street2 as street2,
                                res_partner.city as city,
                                res_country_state.name as state,
                                res_partner.zip as zip,
                                res_country.name as country,
                                res_partner.email as email,
                                delivery_route.location as locname,
                                delivery_route.id as locid

                                                            FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
                                                                         JOIN res_country_state on res_partner.state_id = res_country_state.id
                                                                         JOIN res_country on res_partner.country_id = res_country.id
                                                                         JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
                                                                                      where delivery_route.id = '%s'  """ % (
                    location_val
                ))

            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()

            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'location': location,
                'routes': routes_val

            }
            print(data)
            return \
                self.env.ref(
                    'customer_route_management.route_report_action').report_action(
                    self,
                    data=data)

    # excel start
    def print_xls(self):
        location_val = tuple(self.routes_wizard.mapped('id'))
        routes_val = []
        for rec in self.env['delivery.route.location'].search([]):
            routes_val.append(rec.routes)

        location = []
        for rec in self.routes_wizard:
            location.append(rec.location)

        qy = ("""select res_partner.name as customer,
                                    res_partner.id as cus_id,
                                    delivery_route_location.routes as route,
                                    res_partner.phone as phone,
                                    res_partner.street as street,
                                    res_partner.street2 as street2,
                                    res_partner.city as city,
                                    res_country_state.name as state,
                                    res_partner.zip as zip,
                                    res_country.name as country,
                                    res_partner.email as email,
                                    delivery_route.location as locname,
                                    delivery_route.id as locid

                                                                FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
                                                                             JOIN res_country_state on res_partner.state_id = res_country_state.id
                                                                             JOIN res_country on res_partner.country_id = res_country.id
                                                                             JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
                                                                                          where delivery_route.id in {} """.format(
            tuple(self.routes_wizard.ids)))
        if len(tuple(self.routes_wizard.ids)) == 1:
            qy = ("""select res_partner.name as customer,
                                       res_partner.id as cus_id,
                                       delivery_route_location.routes as route,
                                       res_partner.phone as phone,
                                       res_partner.street as street,
                                       res_partner.street2 as street2,
                                       res_partner.city as city,
                                       res_country_state.name as state,
                                       res_partner.zip as zip,
                                       res_country.name as country,
                                       res_partner.email as email,
                                       delivery_route.location as locname,
                                       delivery_route.id as locid

                                                                   FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
                                                                                JOIN res_country_state on res_partner.state_id = res_country_state.id
                                                                                JOIN res_country on res_partner.country_id = res_country.id
                                                                                JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
                                                                                             where delivery_route.id = '%s'  """ % (
                location_val
            ))
        if self.show_due_amount == True:
            qy = ("""select res_partner.name as customer,
                                        res_partner.id as cus_id,
                                        delivery_route_location.routes as route,
                                        res_partner.phone as phone,
                                        res_partner.street as street,
                                        res_partner.street2 as street2,
                                        res_partner.city as city,
                                        res_country_state.name as state,
                                        res_partner.zip as zip,
                                        res_country.name as country,
                                        res_partner.email as email,
                                        delivery_route.location as locname,
                                        delivery_route.id as locid,
                                        account_move.amount_total as amt,
            							account_move.payment_reference as invoice,
            							account_move.payment_state,
            							account_move.invoice_date_due as inv_date




                                                                    FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
                        														 JOIN res_country_state on res_partner.state_id = res_country_state.id
                        														 JOIN res_country on res_partner.country_id = res_country.id
                        														 JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
                        														 LEFT JOIN account_move on res_partner.id = account_move.partner_id


                                                                                              where delivery_route.id in {} """.format(
                tuple(self.routes_wizard.ids)))
            if len(tuple(self.routes_wizard.ids)) == 1:
                qy = ("""select res_partner.name as customer,
                                            res_partner.id as cus_id,
                                            delivery_route_location.routes as route,
                                            res_partner.phone as phone,
                                            res_partner.street as street,
                                            res_partner.street2 as street2,
                                            res_partner.city as city,
                                            res_country_state.name as state,
                                            res_partner.zip as zip,
                                            res_country.name as country,
                                            res_partner.email as email,
                                            delivery_route.location as locname,
                                            delivery_route.id as locid,
                                            account_move.amount_total as amt,
                							account_move.payment_reference as invoice,
                							account_move.payment_state,
                							account_move.invoice_date_due as inv_date




                                                                        FROM delivery_route_location JOIN res_partner on delivery_route_location.id = routes_inherit_id
                            														 JOIN res_country_state on res_partner.state_id = res_country_state.id
                            														 JOIN res_country on res_partner.country_id = res_country.id
                            														 JOIN delivery_route on delivery_route_location.routes_id = delivery_route.id
                            														 LEFT JOIN account_move on res_partner.id = account_move.partner_id


                                                                                                 where delivery_route.id = '%s'  """ % (
                    location_val
                ))


        self.env.cr.execute(qy)
        qdata = self.env.cr.dictfetchall()
        print(qdata)

        data = {
            'form_data': self.read()[0],
            'query': qdata,
            'location': location,
            'routes': routes_val,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'route.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        # print('get_xlsx_report')

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        show_due_amount = data['form_data']['show_due_amount']
        if show_due_amount == True:
            sheet.write('D7', 'Invoices', cell_format)
            sheet.write('P9', 'Amount', cell_format)

        count = 0
        row = 9
        col = 1
        #

        sheet.merge_range('D2:L3', 'Route Report', head)

        for res in data['query']:

            if show_due_amount:
                if res['invoice']:
                    sheet.write('B9', 'Invoices', cell_format)
                if res['amt']:
                    sheet.write('P9', 'Amount', cell_format)


            sheet.write('D9', 'Customer', cell_format)
            sheet.write('G9', 'Location', cell_format)
            sheet.write('J9', 'Route', cell_format)
            sheet.write('L9', 'Phone', cell_format)
            sheet.write('N9', 'State', cell_format)

            row += 1

            sheet.write(row, col + 2, res['customer'], txt)
            sheet.write(row, col + 5, res['locname'], txt)
            sheet.write(row, col + 8, res['route'], txt)
            sheet.write(row, col + 10, res['phone'], txt)
            sheet.write(row, col + 12, res['street'], txt)
            if show_due_amount:
                if res['invoice']:
                    sheet.write(row, col, res['invoice'], txt)
                else:
                    sheet.write(row, col, 'No invoice', txt)
                if res['amt']:
                    sheet.write(row, col + 14, res['amt'], txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()