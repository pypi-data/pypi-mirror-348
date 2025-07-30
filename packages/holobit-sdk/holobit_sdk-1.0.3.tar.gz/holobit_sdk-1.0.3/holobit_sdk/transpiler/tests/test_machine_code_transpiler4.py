# Archivo: transpiler/tests/test_machine_code_transpiler.py

import unittest
from transpiler.machine_code_transpiler import MachineCodeTranspiler


class TestMachineCodeTranspiler(unittest.TestCase):
    """
    Pruebas unitarias para el módulo MachineCodeTranspiler con soporte para múltiples arquitecturas.
    """

    def setUp(self):
        self.transpiler_x86 = MachineCodeTranspiler("x86")
        self.transpiler_arm = MachineCodeTranspiler("ARM")
        self.transpiler_riscv = MachineCodeTranspiler("RISC-V")

    def test_transpile_allocate_x86(self):
        """ Prueba la transpilación de ALLOCATE en x86. """
        resultado = self.transpiler_x86.transpile("ALLOCATE H1 0.1 0.2 0.3")
        self.assertEqual(resultado, "MOV H1 0.1 0.2 0.3")

    def test_transpile_allocate_arm(self):
        """ Prueba la transpilación de ALLOCATE en ARM. """
        resultado = self.transpiler_arm.transpile("ALLOCATE H1 0.1 0.2 0.3")
        self.assertEqual(resultado, "LDR H1 0.1 0.2 0.3")

    def test_transpile_allocate_riscv(self):
        """ Prueba la transpilación de ALLOCATE en RISC-V. """
        resultado = self.transpiler_riscv.transpile("ALLOCATE H1 0.1 0.2 0.3")
        self.assertEqual(resultado, "LW H1 0.1 0.2 0.3")

    def test_transpile_jump_x86(self):
        """ Prueba la transpilación de JUMP en x86. """
        resultado = self.transpiler_x86.transpile("JUMP LABEL1")
        self.assertEqual(resultado, "JMP LABEL1")

    def test_transpile_jump_arm(self):
        """ Prueba la transpilación de JUMP en ARM. """
        resultado = self.transpiler_arm.transpile("JUMP LABEL1")
        self.assertEqual(resultado, "B LABEL1")

    def test_transpile_jump_riscv(self):
        """ Prueba la transpilación de JUMP en RISC-V. """
        resultado = self.transpiler_riscv.transpile("JUMP LABEL1")
        self.assertEqual(resultado, "JAL LABEL1")


if __name__ == "__main__":
    unittest.main()
