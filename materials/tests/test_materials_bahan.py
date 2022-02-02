# import unittest
from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
from ..models.materials_bahan import MaterialsBahan

class MaterialsTestCase(TransactionCase):
    def setUp(self):
        super(MaterialsTestCase, self).setUp()
        self.materials_obj = self.env['materials.bahan']
    
    def test_materials_model_exists(self):
        self.assertTrue(self.materials_obj._name in self.env)
    
    def test_materials_creates_with_valid_data(self):
        materials = self.materials_obj.create({'code': '001', 'name': 'Celana', 'type':'jeans', 'buy_price': 1000, 'supplier_id':1})
        self.assertTrue(bool(self.materials_obj.search([('id', '=', materials.id)], limit=1)))
    
    def test_materials_creation_throws_exception_with_invalid_data(self):
        with self.assertRaises(ValidationError):
            self.materials_obj.create({'code': 1000, 'name': 1, 'type':'jeans', 'buy_price': 90, 'supplier_id':1})