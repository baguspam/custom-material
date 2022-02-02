from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from . import materials_supplier

class MaterialsBahan(models.Model):
    _name = 'materials.bahan'

    code = fields.Char(string='Kode', required=True)
    name = fields.Char(string='Nama', required=True)
    type = fields.Selection(
        selection=[
            ('fabric', 'Fabric'),
            ('jeans', 'Jeans'),
            ('cotton', 'Cotton'),
            ],
        string='Tipe Bahan')
    buy_price = fields.Integer(string='Harga Beli', required=True, default=100)
    supplier_id = fields.Many2one(comodel_name='materials.supplier', string='Supplier')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Nomor Kode sudah Ada !')
    ]

    @api.onchange('buy_price')
    def get_buy_price(self):
        if self.buy_price >=100:
            self.buy_price = self.buy_price
        else:
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Cek Kembali Kolom Harga Beli, Harga Beli tidak boleh < 100',
                }
            }
    
    @api.constrains('buy_price')
    def check_buy_price(self):
        if self.buy_price <100:
            raise ValidationError('Harga Beli tidak boleh < 100')
    
    @api.depends('buy_price')
    def save_buy_price(self):
        self.buy_price = self.buy_price