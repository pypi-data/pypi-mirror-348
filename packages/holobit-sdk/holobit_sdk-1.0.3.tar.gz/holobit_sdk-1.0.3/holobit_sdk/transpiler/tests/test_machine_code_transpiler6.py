# Archivo: transpiler/tests/test_machine_code_transpiler.py

import unittest
from transpiler.machine_code_transpiler import MachineCodeTranspiler


class TestMachineCodeTranspiler(unittest.TestCase):
    """
    Pruebas unitarias para el módulo MachineCodeTranspiler con soporte optimizado para múltiples arquitecturas.
    """

    def setUp(self):
        self.transpiler_x86 = MachineCodeTranspiler("x86")
        self.transpiler_arm = MachineCodeTranspiler("ARM")
        self.transpiler_riscv = MachineCodeTranspiler("RISC-V")

    def test_transpile_allocate_x86(self):
        """ Prueba la transpilación de ALLOCATE en x86. """
        resultado = self.transpiler_x86.transpile("ALLOCATE H1 0.1 0.2 0.3")
        self.assertEqual(resultado, "MOV H1 0.1 0.2 0.3")

    def test_transpile_jump_x86_optimized(self):
        """ Prueba la optimización de JUMP en x86. """
        resultado = self.transpiler_x86.transpile("JUMP LABEL1")
        self.assertEqual(resultado, "JMP LABEL1")

    def test_transpile_compare_redundant(self):
        """ Prueba la eliminación de comparaciones redundantes. """
        resultado = self.transpiler_x86.transpile("COMPARE H1 H1")
        self.assertEqual(resultado, "NOP")

    def test_transpile_clear_register_x86(self):
        """ Prueba la optimización de registros redundantes en x86. """
        resultado = self.transpiler_x86.transpile("ADD H1 H1")
        self.assertEqual(resultado, "CLEAR H1")

    def test_transpile_clear_register_riscv(self):
        """ Prueba la optimización de registros redundantes en RISC-V. """
        resultado = self.transpiler_riscv.transpile("SUB H2 H2")
        self.assertEqual(resultado, "CLEAR H2")

    def test_transpile_mult_x86(self):
        """ Prueba la transpilación de MULT en x86. """
        resultado = self.transpiler_x86.transpile("MULT H1 H2")
        self.assertEqual(resultado, "MUL H1 H2")

    def test_transpile_div_arm(self):
        """ Prueba la transpilación de DIV en ARM. """
        resultado = self.transpiler_arm.transpile("DIV H1 H2")
        self.assertEqual(resultado, "DIV_ARM H1 H2")

    def test_transpile_push_riscv(self):
        """ Prueba la transpilación de PUSH en RISC-V. """
        resultado = self.transpiler_riscv.transpile("PUSH H1")
        self.assertEqual(resultado, "PUSH_RV H1")

    def test_transpile_pop_riscv(self):
        """ Prueba la transpilación de POP en RISC-V. """
        resultado = self.transpiler_riscv.transpile("POP H1")
        self.assertEqual(resultado, "POP_RV H1")


if __name__ == "__main__":
    unittest.main()
