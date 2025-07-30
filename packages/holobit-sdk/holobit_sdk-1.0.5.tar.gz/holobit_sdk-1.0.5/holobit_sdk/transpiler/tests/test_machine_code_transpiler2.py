import unittest
from transpiler.machine_code_transpiler import MachineCodeTranspiler


class TestMachineCodeTranspiler(unittest.TestCase):
    """
    Pruebas unitarias para el módulo MachineCodeTranspiler.
    """

    def setUp(self):
        self.transpiler = MachineCodeTranspiler()

    def test_transpile_complex_instruction(self):
        """ Prueba la transpilación de una instrucción compleja. """
        resultado = self.transpiler.transpile("ALLOCATE H1 H2 0.5 0.6 0.7")
        self.assertEqual(resultado, "MOV H1 H2 0.5 0.6 0.7")


if __name__ == "__main__":
    unittest.main()
