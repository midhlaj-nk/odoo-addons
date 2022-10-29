from odoo import fields, models, api
from odoo.exceptions import ValidationError


class rentalrequest(models.Model):
    _name = "rental.request"
    _description = "Rental Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_id = fields.Many2one('rental.vehicle',
                                 domain="[('state','=','available')]",
                                 required=True)

    name = fields.Char(string='Order Reference', required=True,
                       readonly=True, default=lambda self: 'New')
    customer = fields.Many2one('res.partner', required=True)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    rent_amount = fields.Monetary(string="Rent Fee",
                                  related='period_type.rent_amount_prtype',
                                  store=True)
    period_type = fields.Many2one('rent.charges')
    count = fields.Integer(compute="count_invoice")

    # period type selection
    @api.onchange('vehicle_id')
    def period_type_values(self):
        print("type work")
        a = int(self.vehicle_id)
        print(a)
        return {'domain': {'period_type':[('vehicle_id', '=', a)]}}

    state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('confirm', 'Confirm'), ('returned', 'Returned'),
                   ('invoiced', 'Invoiced')],
        default='draft')
    request_date = fields.Date(default=fields.Date.today)
    from_date = fields.Date(String="From", required=True)
    to_date = fields.Date(String="to", required=True)
    period = fields.Char(String="Period")

    # invoice button
    def invoice(self):
        vals = []
        for record in self:
            print(self.env['prescription.line'],'kdpoakpodapodka')
            vals.append((0, 0,
                         {'name': record.vehicle_id.model_id.name,
                          'price_unit': record.rent_amount,
                          }))
            print(vals)
        invoice = self.env['account.move'].create([
            {'move_type': 'out_invoice',
             'partner_id': self.customer,
             'ref': self.name,
             'invoice_date': fields.Date.today(),
             'invoice_line_ids': vals
             }, ])

        return {
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
        }

    def invoice_button(self):
        return {
            'res_model': 'account.move',
            'name': 'Rental invoices',
            'view_mode': 'tree,form',
            'domain': [('ref', '=', self.name)],
            'type': 'ir.actions.act_window',
        }

    # button confrim
    def button_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            rec.vehicle_id.state = 'not available'

    # button return
    def button_return(self):
        for rec in self:
            rec.state = 'returned'
            rec.vehicle_id.state = 'available'

            # sequence number

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'rental.request') or 'New'
        res = super(rentalrequest, self).create(vals)
        return res

    # From to date

    @api.onchange('from_date', 'to_date', 'period', 'period_type')
    def calculate_date(self):
        for rec in self:
            rec.period = 0
            if rec.from_date and rec.to_date:
                d1 = rec.from_date
                d2 = rec.to_date
                d3 = str((d2 - d1).days)
                rec.period = int(d3)
                c = int(d3)
                period_x = self.period_type.period_type
                print(period_x)
                if period_x == 'hour':
                    rec.period = c * 24
                if period_x == 'day':
                    rec.period = c
                if period_x == 'week':
                    if (c % 7) == 0:
                        period = c / 7
                        rec.period = round(period)
                    else:
                        period = c / 7
                        rec.period = round(period + 1)
                if period_x == 'month':
                    if (c % 30) == 0:
                        period = c // 30
                        rec.period = period
                    else:
                        period = c // 30
                        rec.period = (period + 1)

    @api.onchange('period')
    def calculate_rent(self):
        for rec in self:
            if rec.from_date and rec.to_date:
                rec.rent_amount = int(rec.rent_amount) + int(rec.period)
                print('final amount', rec.rent_amount)

    # Greater or less than
    @api.onchange('to_date', 'from_date')
    def check_values(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError(
                    'The To date should be Greater than from date')

    # invoices count
    def count_invoice(self):
        self.count = self.env['account.move'].search_count(
            [('ref', '=', self.name)])


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        # print(self.payment_state)
        # print(self.ref)
        request = self.env['rental.request'].search([('name', '=', self.ref)])
        request.state = 'invoiced'
        # print(request.state)
        res = super(AccountMove, self).action_post()
        return res
