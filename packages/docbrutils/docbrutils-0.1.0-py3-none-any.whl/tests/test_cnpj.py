
import unittest
from docbrutils import cnpj

class TestCNPJ(unittest.TestCase):
    def test_validate_valid(self):
        self.assertTrue(cnpj.validate_cnpj(cnpj.generate_cnpj()))

    def test_validate_invalid(self):
        self.assertFalse(cnpj.validate_cnpj("00.000.000/0000-00"))
