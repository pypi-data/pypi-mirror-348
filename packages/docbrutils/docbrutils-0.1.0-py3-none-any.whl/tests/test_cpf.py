
import unittest
from docbrutils import cpf

class TestCPF(unittest.TestCase):
    def test_validate_valid(self):
        self.assertTrue(cpf.validate_cpf(cpf.generate_cpf()))

    def test_validate_invalid(self):
        self.assertFalse(cpf.validate_cpf("111.111.111-11"))
