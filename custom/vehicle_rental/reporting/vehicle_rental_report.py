import json
import io
from odoo import fields, models
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class VehicleRentalReporting(models.TransientModel):
    _name = 'vehicle.rental.reporting'
    _description = 'Reporting wizard'

    vehicle_id = fields.Many2one('rental.vehicle')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def print_report(self):
        # print("okok")
        # print(self.read())
        if not self.vehicle_id:
            if not self.date_from:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                          res_partner.name as customer,
                                                                          fleet_vehicle.name,
                                                                          rent_charges.period_type,
                                                                          rent_amount,
                                                                          rental_request.state
                                            FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                                JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                                JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                                JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id""")
                else:
                    qy=("""SELECT rental_request.name,
                                                                         res_partner.name as customer,
                                                                         fleet_vehicle.name,
                                                                         rent_charges.period_type,
                                                                         rent_amount,
                                                                         rental_request.state
                                           FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                               JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                               JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                               JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                           where to_date <= '%s'   """ % (
                        self.date_to))
            else:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                        res_partner.name as customer,
                                                                        fleet_vehicle.name,
                                                                        rent_charges.period_type,
                                                                        rent_amount,
                                                                        rental_request.state
                                          FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                              JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                              JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                              JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                          where from_date >= '%s'   """ % (
                        self.date_from))
                else:
                    qy=("""SELECT rental_request.name,
                                                                          res_partner.name as customer,
                                                                          fleet_vehicle.name,
                                                                          rent_charges.period_type,
                                                                          rent_amount,
                                                                          rental_request.state
                                            FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                                JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                                JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                                JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                            where from_date >= '%s' and to_date <= '%s'   """ % (
                        self.date_from,
                        self.date_to))
        else:
            if not self.date_from:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                          res_partner.name as customer,
                                                                          fleet_vehicle.name,
                                                                          rent_charges.period_type,
                                                                          rent_amount,
                                                                          rental_request.state
                                            FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                                JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                                JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                                JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                                                where rental_request.vehicle_id = %s""" % self.vehicle_id.id)
                else:
                    qy=("""SELECT rental_request.name,
                                                                         res_partner.name as customer,
                                                                         fleet_vehicle.name,
                                                                         rent_charges.period_type,
                                                                         rent_amount,
                                                                         rental_request.state
                                           FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                               JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                               JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                               JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                           where rental_request.vehicle_id = %s and to_date <= '%s'   """ % (
                        self.vehicle_id.id,
                        self.date_to))
            else:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                        res_partner.name as customer,
                                                                        fleet_vehicle.name,
                                                                        rent_charges.period_type,
                                                                        rent_amount,
                                                                        rental_request.state
                                          FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                              JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                              JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                              JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                          where rental_request.vehicle_id = %s and from_date >= '%s'   """ % (
                        self.vehicle_id.id,
                        self.date_from))
                else:
                    qy=("""SELECT rental_request.name,
                                                  res_partner.name as customer,
                                                  fleet_vehicle.name,
                                                  rent_charges.period_type,
                                                  rent_amount,
                                                  rental_request.state
                        FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                        JOIN rent_charges on rental_request.period_type=rent_charges.id
                                        JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                        JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                    where rental_request.vehicle_id = %s and from_date >= '%s' and to_date <= '%s'   """ % (
                        self.vehicle_id.id,
                        self.date_from,
                        self.date_to))
        self.env.cr.execute(qy)
        qdata = self.env.cr.dictfetchall()
        print(qdata)
        data = {
            'form_data': self.read()[0],
            'query': qdata
        }
        return \
            self.env.ref(
                'vehicle_rental.action_report_vehicle_rental').report_action(
                self,
                data=data)

    # excel start
    def excel_report(self):
        if not self.vehicle_id:
            if not self.date_from:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                          res_partner.name as customer,
                                                                          fleet_vehicle.name,
                                                                          rent_charges.period_type,
                                                                          rent_amount,
                                                                          rental_request.state
                                            FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                                JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                                JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                                JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id""")
                else:
                    qy=("""SELECT rental_request.name,
                                                                         res_partner.name as customer,
                                                                         fleet_vehicle.name,
                                                                         rent_charges.period_type,
                                                                         rent_amount,
                                                                         rental_request.state
                                           FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                               JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                               JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                               JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                           where to_date <= '%s'   """ % (
                        self.date_to))
            else:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                        res_partner.name as customer,
                                                                        fleet_vehicle.name,
                                                                        rent_charges.period_type,
                                                                        rent_amount,
                                                                        rental_request.state
                                          FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                              JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                              JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                              JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                          where from_date >= '%s'   """ % (
                        self.date_from))
                else:
                    qy=("""SELECT rental_request.name,
                                                                          res_partner.name as customer,
                                                                          fleet_vehicle.name,
                                                                          rent_charges.period_type,
                                                                          rent_amount,
                                                                          rental_request.state
                                            FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                                JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                                JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                                JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                            where from_date >= '%s' and to_date <= '%s'   """ % (
                        self.date_from,
                        self.date_to))
        else:
            if not self.date_from:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                          res_partner.name as customer,
                                                                          fleet_vehicle.name,
                                                                          rent_charges.period_type,
                                                                          rent_amount,
                                                                          rental_request.state
                                            FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                                JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                                JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                                JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                                                where rental_request.vehicle_id = %s""" % self.vehicle_id.id)
                else:
                    qy=("""SELECT rental_request.name,
                                                                         res_partner.name as customer,
                                                                         fleet_vehicle.name,
                                                                         rent_charges.period_type,
                                                                         rent_amount,
                                                                         rental_request.state
                                           FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                               JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                               JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                               JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                           where rental_request.vehicle_id = %s and to_date <= '%s'   """ % (
                        self.vehicle_id.id,
                        self.date_to))
            else:
                if not self.date_to:
                    qy=("""SELECT rental_request.name,
                                                                        res_partner.name as customer,
                                                                        fleet_vehicle.name,
                                                                        rent_charges.period_type,
                                                                        rent_amount,
                                                                        rental_request.state
                                          FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                                              JOIN rent_charges on rental_request.period_type=rent_charges.id
                                                              JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                                              JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                                          where rental_request.vehicle_id = %s and from_date >= '%s'   """ % (
                        self.vehicle_id.id,
                        self.date_from))
                else:
                    qy=("""SELECT rental_request.name,
                                                  res_partner.name as customer,
                                                  fleet_vehicle.name,
                                                  rent_charges.period_type,
                                                  rent_amount,
                                                  rental_request.state
                    FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
                                        JOIN rent_charges on rental_request.period_type=rent_charges.id
                                        JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
                                        JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
                    where rental_request.vehicle_id = %s and from_date >= '%s' and to_date <= '%s'   """ % (
                        self.vehicle_id.id,
                        self.date_from,
                        self.date_to))
        self.env.cr.execute(qy)
        qdata = self.env.cr.dictfetchall()
        print(qdata)
        data = {
            'form_data': self.read()[0],
            'query': qdata
        }
        # if self.date_from > self.date_to:
        #     raise ValidationError('Start Date must be less than End Date')
        #
        # self.env.cr.execute("""SELECT rental_request.name,
        #                                                   res_partner.name as customer,
        #                                                   fleet_vehicle.name,
        #                                                   rent_charges.period_type,
        #                                                   rent_amount,
        #                                                   rental_request.state
        # FROM rental_request JOIN res_partner on rental_request.customer=res_partner.id
        #                     JOIN rent_charges on rental_request.period_type=rent_charges.id
        #                     JOIN rental_vehicle on rental_request.vehicle_id=rental_vehicle.id
        #                     JOIN fleet_vehicle on rental_vehicle.model_id=fleet_vehicle.id
        # where from_date >= '%s' and to_date <= '%s'   """ % (
        #     self.date_from,
        #     self.date_to))
        # qdata = self.env.cr.dictfetchall()
        # print(qdata)
        # data = {
        #     'form_data': self.read()[0],
        #
        #     'query': qdata
        # }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'vehicle.rental.reporting',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print(data)
        # print('get_xlsx_report')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('D2:L3', 'Vehicle Report', head)
        wizard_data = data['form_data']

        if wizard_data['vehicle_id']:
            sheet.write('D4', 'Vehicle Name', cell_format)
            sheet.write('F4', wizard_data['vehicle_id'][1])

        if wizard_data['date_to']:
            sheet.write('D5', 'From Date', cell_format)
            sheet.write('F5', wizard_data['date_from'])
        if wizard_data['date_from']:
            sheet.write('D6', 'To Date', cell_format)
            sheet.write('F6', wizard_data['date_to'])

        sheet.write('B9', 'Sl no.', cell_format)
        sheet.write('D9', 'Customer', cell_format)
        sheet.write('G9', 'Vehicle Name', cell_format)
        sheet.write('J9', 'Period Type', cell_format)
        sheet.write('L9', 'Rent amount', cell_format)
        sheet.write('N9', 'State', cell_format)

        count = 0
        row = 9
        col = 1
        for res in data['query']:
            row += 1
            sheet.write(row, col, count, txt)
            sheet.write(row, col + 2, res['customer'], txt)
            sheet.write(row, col + 5, res['name'], txt)
            sheet.write(row, col + 8, res['period_type'], txt)
            sheet.write(row, col + 11, res['rent_amount'], txt)
            sheet.write(row, col + 12, res['state'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
