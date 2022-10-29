from odoo import fields, models, api


class MaterialRequest(models.Model):
    _name = 'material.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Order Reference', required=True,
                       readonly=True, default=lambda self: 'New')
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    material_request_line_ids = fields.One2many('material.request.line',
                                                'request_id')

    state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('approval_manager', 'Approval By Manager'),
                   ('approval_head', 'Approval By Head'),
                   ('request_accepted', 'Request Accepted'),
                   ('reject', 'Reject')],
        default='draft')

    def button_confirm(self):
        self.state = 'approval_manager'

    def button_approve_manager(self):
        self.state = 'approval_head'

    def button_approve_head(self):

        self.state = 'request_accepted'
        for record in self.material_request_line_ids:
            if record.delivery_type == "purchase_order":
                for rec in record.product_id.variant_seller_ids.name:
                    self.env['purchase.order'].create([
                        {'partner_id': rec.id,
                         'order_line': [((0, 0, {
                             'product_id': record.product_id.id,
                             'product_qty': record.quantity}))],
                         }, ])
            else:
                record.env[
                    'stock.picking'].create(
                    [
                        {'picking_type_id': 5,
                         'location_id': record.location_id.id,
                         'location_dest_id': record.location_dest_id.id,
                         'move_ids_without_package': [(0, 0,
                                                       {
                                                           'product_id': record.product_id.id,
                                                           'name': record.product_id.id,
                                                           'product_uom': record.product_id.uom_id,
                                                           'location_id': record.location_id.id,
                                                           'location_dest_id': record.location_dest_id.id,
                                                           'product_uom_qty': record.quantity,
                                                       },), ]
                         }, ])

    def button_reject_head(self):
        for rec in self:
            rec.state = 'reject'

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'material.request') or 'New'
        res = super(MaterialRequest, self).create(vals)
        return res


class ProductRequest(models.Model):
    _name = 'material.request.line'

    location_id = fields.Many2one(
        'stock.location', "Source Location")
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location")
    delivery_type = fields.Selection(
        selection=[('purchase_order', 'Purchase Order'),
                   ('internal_transfer', 'Internal Transfer')])
    product_id = fields.Many2one('product.product')
    request_id = fields.Many2one('material.request')
    quantity = fields.Integer()


