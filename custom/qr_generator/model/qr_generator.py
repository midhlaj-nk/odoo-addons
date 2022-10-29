try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class QrGenerator(models.TransientModel):
    _name = 'qr.generator'
    _rec_name = 'text'

    text = fields.Char('Input Text Here')
    qr_code = fields.Binary('QrCode')

    def generate(self):
        # "method to generate QR code"
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(rec.text)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
                return {
                    'context': self.env.context,
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'qr.generator',
                    'res_id': self.id,
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                }

    def reset(self):
        if self.qr_code or self.text:
            self.text = ''
            self.qr_code = None
            return {
                'context': self.env.context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'qr.generator',
                'res_id': self.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }

    def download(self):
        data = {
            'form_data': self.read()[0]
        }
        print(data)
        return self.env.ref(
            'qr_generator.action_image').report_action(
            self,
            data=data)
