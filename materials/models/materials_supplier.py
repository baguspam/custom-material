from odoo import models, fields, _

class MaterialsSupplier(models.Model):
    _name = 'materials.supplier'

    name = fields.Char(string='Nama Supplier', required=True)
    address = fields.Text(string='Alamat')