# Archivo: multi_level/high_level/tests/test_compiler.py

import unittest
from multi_level.high_level.compiler import HoloLangCompiler


class TestHoloLangCompiler(unittest.TestCase):
    """
    Pruebas unitarias para la integración del compilador con el transpilador.
    """

    def setUp(self):
        self.compiler_x86 = HoloLangCompiler("x86")
        self.compiler_arm = HoloLangCompiler("ARM")
        self.compiler_riscv = HoloLangCompiler("RISC-V")

    def test_crear_variable(self):
        """ Prueba la creación de variables en HoloLang. """
        resultado = self.compiler_x86.compilar_y_ejecutar("CREAR H1 (0.1, 0.2, 0.3)")
        self.assertEqual(resultado, "Variable H1 creada con valores (0.1, 0.2, 0.3)")

    def test_imprimir_variable(self):
        """ Prueba la impresión de variables en HoloLang. """
        self.compiler_x86.compilar_y_ejecutar("CREAR H2 (0.4, 0.5, 0.6)")
        resultado = self.compiler_x86.compilar_y_ejecutar("IMPRIMIR H2")
        self.assertEqual(resultado, "H2 = (0.4, 0.5, 0.6)")

    def test_compilar_y_transpilar_x86(self):
        """ Prueba la compilación y transpilación en x86. """
        resultado = self.compiler_x86.compilar_y_ejecutar("EJECUTAR MULT H1 H2")
        self.assertEqual(resultado, "Código máquina generado: MUL H1 H2")

    def test_compilar_y_transpilar_arm(self):
        """ Prueba la compilación y transpilación en ARM. """
        resultado = self.compiler_arm.compilar_y_ejecutar("EJECUTAR DIV H1 H2")
        self.assertEqual(resultado, "Código máquina generado: DIV_ARM H1 H2")

    def test_compilar_y_transpilar_riscv(self):
        """ Prueba la compilación y transpilación en RISC-V. """
        resultado = self.compiler_riscv.compilar_y_ejecutar("EJECUTAR PUSH H1")
        self.assertEqual(resultado, "Código máquina generado: PUSH_RV H1")


if __name__ == "__main__":
    unittest.main()
