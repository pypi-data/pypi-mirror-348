# Archivo: transpiler/tests/test_machine_code_transpiler.py

import unittest
from transpiler.machine_code_transpiler import MachineCodeTranspiler


class TestMachineCodeTranspiler(unittest.TestCase):
    """
    Pruebas unitarias para el módulo MachineCodeTranspiler.
    """

    def setUp(self):
        self.transpiler = MachineCodeTranspiler()

    def test_transpile_allocate(self):
        """ Prueba la transpilación de la instrucción ALLOCATE. """
        resultado = self.transpiler.transpile("ALLOCATE H1 0.1 0.2 0.3")
        self.assertEqual(resultado, "MOV H1 0.1 0.2 0.3")

    def test_transpile_get_position(self):
        """ Prueba la transpilación de la instrucción GET_POSITION. """
        resultado = self.transpiler.transpile("GET_POSITION H1")
        self.assertEqual(resultado, "READ_POS H1")

    def test_transpile_deallocate(self):
        """ Prueba la transpilación de la instrucción DEALLOCATE. """
        resultado = self.transpiler.transpile("DEALLOCATE H1")
        self.assertEqual(resultado, "FREE H1")

    def test_transpile_rotate(self):
        """ Prueba la transpilación de la instrucción ROTATE. """
        resultado = self.transpiler.transpile("ROTATE H1 z 90")
        self.assertEqual(resultado, "ROT H1 z 90")

    def test_transpile_link(self):
        """ Prueba la transpilación de la instrucción LINK. """
        resultado = self.transpiler.transpile("LINK H1 H2")
        self.assertEqual(resultado, "LINK H1 H2")

    def test_transpile_unlink(self):
        """ Prueba la transpilación de la instrucción UNLINK. """
        resultado = self.transpiler.transpile("UNLINK H1 H2")
        self.assertEqual(resultado, "UNLINK H1 H2")

    def test_transpile_jump(self):
        """ Prueba la transpilación de la instrucción JUMP. """
        resultado = self.transpiler.transpile("JUMP LABEL1")
        self.assertEqual(resultado, "JMP LABEL1")

    def test_transpile_compare(self):
        """ Prueba la transpilación de la instrucción COMPARE. """
        resultado = self.transpiler.transpile("COMPARE H1 H2")
        self.assertEqual(resultado, "CMP H1 H2")

    def test_transpile_add(self):
        """ Prueba la transpilación de la instrucción ADD. """
        resultado = self.transpiler.transpile("ADD H1 H2")
        self.assertEqual(resultado, "ADD H1 H2")

    def test_transpile_sub(self):
        """ Prueba la transpilación de la instrucción SUB. """
        resultado = self.transpiler.transpile("SUB H1 H2")
        self.assertEqual(resultado, "SUB H1 H2")

    def test_transpile_unknown_instruction(self):
        """ Prueba la transpilación de una instrucción desconocida. """
        resultado = self.transpiler.transpile("UNKNOWN_CMD H1")
        self.assertEqual(resultado, "Instrucción holográfica desconocida: UNKNOWN_CMD")


if __name__ == "__main__":
    unittest.main()
