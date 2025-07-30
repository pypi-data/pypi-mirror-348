import unittest
from asiic_holographic.interpreter import ASIICInterpreter
from asiic_holographic.translator import ASIICTranslator
from asiic_holographic.instructions import ASIICInstructions



class TestASIIC(unittest.TestCase):
    """
    Pruebas unitarias para el ASIIC Holográfico.
    """

    def setUp(self):
        """ Configuración inicial para las pruebas. """
        self.interpreter = ASIICInterpreter()
        self.translator = ASIICTranslator()

    def test_interpretar_rotar(self):
        """ Verifica que la instrucción ROTAR se interpreta correctamente. """
        resultado = self.interpreter.interpretar("ROTAR H1 z 90")
        self.assertEqual(resultado, "Rotando Holobit H1 en el eje z con 90 grados")

    def test_interpretar_entrelazar(self):
        """ Verifica que la instrucción ENTRELAZAR se interpreta correctamente. """
        resultado = self.interpreter.interpretar("ENTRELAZAR H1 H2")
        self.assertEqual(resultado, "Entrelazando Holobits H1 y H2")

    def test_traducir_rotar(self):
        """ Verifica que la instrucción ROTAR se traduce correctamente a ensamblador. """
        resultado = self.translator.traducir("ROTAR H1 z 90")
        self.assertEqual(resultado, "ROT H1 z 90")

    def test_traducir_entrelazar(self):
        """ Verifica que la instrucción ENTRELAZAR se traduce correctamente a ensamblador. """
        resultado = self.translator.traducir("ENTRELAZAR H1 H2")
        self.assertEqual(resultado, "ENTR H1 H2")

    def test_instruccion_desconocida(self):
        """ Verifica que una instrucción desconocida sea manejada correctamente. """
        resultado = self.translator.traducir("DESCONOCIDO X Y Z")
        self.assertEqual(resultado, "Instrucción desconocida: DESCONOCIDO")


if __name__ == "__main__":
    unittest.main()
