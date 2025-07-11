import unittest
from pricing_logic.material_db import get_material_cost
from pricing_logic.labor_calc import calculate_labor_cost, estimate_labor_time
from pricing_logic.vat_rules import get_vat_rate, apply_vat

class TestPricingLogic(unittest.TestCase):
    def test_material_cost(self):
        # Tests if the material cost for 'remove tiles' is correctly returned as 100
        self.assertEqual(get_material_cost('remove tiles'), 100)

    def test_labor_cost(self):
        # Verifies that labor cost calculation works properly
        # 5 hours of labor at 50 per hour should be 250
        self.assertEqual(calculate_labor_cost(5, 50), 250)

    def test_vat_rate(self):
        # Checks if the VAT rate for Marseille is correctly returned as 20%
        self.assertEqual(get_vat_rate('Marseille'), 0.20)

    def test_apply_vat(self):
        # Tests the VAT application function
        # 100 with 20% VAT should be 120
        self.assertEqual(apply_vat(100, 0.20), 120)

if __name__ == '__main__':
    # Runs the test suite when this file is executed directly
    unittest.main()