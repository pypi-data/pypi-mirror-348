# Archivo: transpiler/tests/test_machine_code_transpiler.py

import unittest
from transpiler.machine_code_transpiler import MachineCodeTranspiler


class TestMachineCodeTranspiler(unittest.TestCase):
    """
    Pruebas unitarias para el módulo MachineCodeTranspiler con optimización avanzada.
    """

    def setUp(self):
        self.transpiler_x86 = MachineCodeTranspiler("x86")
        self.transpiler_arm = MachineCodeTranspiler("ARM")
        self.transpiler_riscv = MachineCodeTranspiler("RISC-V")

    def test_transpile_allocate_x86(self):
        """ Prueba la transpilación de ALLOCATE en x86. """
        resultado = self.transpiler_x86.transpile("ALLOCATE H1 0.1 0.2 0.3")
        self.assertEqual(resultado, "MOV H1 0.1 0.2 0.3")

    def test_transpile_jump_optimized(self):
        """ Prueba la optimización de JUMP en x86. """
        resultado = self.transpiler_x86.transpile("JUMP NEXT")
        self.assertEqual(resultado, "JMP NEXT")

    def test_transpile_compare_redundant(self):
        """ Prueba la eliminación de comparaciones redundantes. """
        resultado = self.transpiler_x86.transpile("COMPARE H1 H1")
        self.assertEqual(resultado, "NOP")

    def test_transpile_clear_register(self):
        """ Prueba la optimización de registros redundantes. """
        resultado = self.transpiler_x86.transpile("MULT H1 H1")
        self.assertEqual(resultado, "CLEAR H1")

    def test_transpile_push_multi(self):
        """ Prueba la optimización de PUSH para múltiples registros. """
        resultado = self.transpiler_x86.transpile("PUSH H1 H2 H3")
        self.assertEqual(resultado, "PUSH_MULTI H1 H2 H3")

    def test_transpile_pop_multi(self):
        """ Prueba la optimización de POP para múltiples registros. """
        resultado = self.transpiler_x86.transpile("POP H1 H2 H3")
        self.assertEqual(resultado, "POP_MULTI H1 H2 H3")


if __name__ == "__main__":
    unittest.main()
