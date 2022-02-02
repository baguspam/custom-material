# import unittest
from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
from ..models.materials_supplier import MaterialsSupplier

class MaterialsSupplierTestCase(TransactionCase):
    def setUp(self):
        super(MaterialsSupplierTestCase, self).setUp()
        self.materials_obj = self.env['materials.supplier']
    
    def test_supplier_model_exists(self):
        self.assertTrue(self.materials_obj._name in self.env)
    
    def test_supplier_creates_with_valid_data(self):
        materials = self.materials_obj.create({'name': 'PT. Fabric', 'address':'Jl. Kunciran 9'})
        self.assertTrue(bool(self.materials_obj.search([('id', '=', materials.id)], limit=1)))