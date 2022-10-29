from odoo import fields, models, api
from datetime import timedelta


class RentalVehicle(models.Model):
    _name = "rental.vehicle"
    _description = "Rental Vehicle"
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute='_compute_vehicle_name')
    model_id = fields.Many2one('fleet.vehicle')
    brand_id = fields.Many2one('fleet.vehicle.model.brand', 'Brand',
                               related="model_id.brand_id")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    # rent_amount = fields.Monetary(string="Rent Fee")
    state = fields.Selection(
        selection=[('available', 'Available'),
                   ('not available', 'Not Available'), ('sold', 'Sold')],
        default='available', store=True)
    reg_date = fields.Date(related='model_id.reg_date1',
                           string="Registered Date", readonly=False,
                           default=fields.Date.today())
    model_year = fields.Char()
    vehicle_request_specific = fields.Char(compute="count")
    requests_inpage = fields.One2many('rental.request', 'vehicle_id',
                                      readonly=True)
    #requests_inpage domain = [('state', '=', 'confirm')]
    rentcharge_ids = fields.One2many('rent.charges', 'vehicle_id',
                                     string="Charges")
    customer = fields.Many2one('res.partner')
    warning = fields.Boolean()
    late = fields.Boolean()

    # TO DATE WARNING ()
    def warnlatecheck(self):
        records = self.search([
            ('state', '=', 'not available')
        ])
        for rec in records:
            fetch_2_date_record = self.env['rental.request'].search(
                [('vehicle_id', '=', rec.id)])
            tdate = fetch_2_date_record.to_date
            vehicle_state = self.env['rental.request'].search(
                [('vehicle_id', '=', rec.id)])
            vstate = vehicle_state.state
            if tdate == fields.Date.today() - timedelta(days=2):
                rec.warning = False
                print("if inside",rec.warning)

            else:
                rec.warning = True
                print("else inside",rec.warning)

            if (str(tdate) >= str(fields.Date.today())) and vstate != 'returned':
                rec.late = True


    @api.onchange('reg_date')
    def _compute_year(self):
        if self.reg_date:
            self.model_year = self.reg_date.year

    @api.onchange('model_id')
    def registration_date_visible(self):
        self.reg_date = self.model_id.reg_date1

    @api.onchange('model_id.brand_id.name', 'model_id.name')
    def _compute_vehicle_name(self):
        for rec in self:
            rec.name = rec.brand_id.name + '/' + \
                       rec.model_id.model_id.name + '/' + rec.model_year

    def get_vehicles(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'name': 'Requests',
            'view_mode': 'list,form',
            'res_model': 'rental.request',
            'domain': [('vehicle_id', '=', self.id)],

        }

    def count(self):
        for rec in self:
            rec.vehicle_request_specific = self.env[
                'rental.request'].search_count([('vehicle_id', '=', rec.id)])


class RentCharges(models.Model):
    _name = "rent.charges"
    _description = "Rent Charges"
    _rec_name = "period_type"

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    vehicle_id = fields.Many2one('rental.vehicle')
    period_type = fields.Selection(
        selection=[('hour', 'Hour'),
                   ('day', 'Day'), ('week', 'Week'), ('month', 'Month')])
    rent_amount_prtype = fields.Monetary(string="Rent Fee")
