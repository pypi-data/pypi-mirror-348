import unittest
from multi_level.low_level.memory_manager import MemoryManager
from multi_level.low_level.low_level_api import LowLevelAPI
from multi_level.low_level.execution_unit import ExecutionUnit


class TestLowLevel(unittest.TestCase):
    """
    Pruebas unitarias para el Nivel Bajo del SDK Holobit.
    """

    def setUp(self):
        self.memory = MemoryManager()
        self.api = LowLevelAPI()
        self.executor = ExecutionUnit()

    def test_allocate_holobit(self):
        """ Prueba la asignación de un Holobit en la memoria. """
        resultado = self.api.ejecutar_comando("ALLOCATE", "H1", 0.1, 0.2, 0.3)
        self.assertEqual(resultado, "Holobit H1 asignado en (0.1, 0.2, 0.3).")

    def test_get_position_holobit(self):
        """ Prueba la obtención de la posición de un Holobit. """
        self.api.ejecutar_comando("ALLOCATE", "H1", 0.1, 0.2, 0.3)
        resultado = self.api.ejecutar_comando("GET_POSITION", "H1")
        self.assertEqual(resultado, "Posición de H1: (0.1, 0.2, 0.3)")

    def test_deallocate_holobit(self):
        """ Prueba la liberación de un Holobit en la memoria. """
        self.api.ejecutar_comando("ALLOCATE", "H1", 0.1, 0.2, 0.3)
        resultado = self.api.ejecutar_comando("DEALLOCATE", "H1")
        self.assertEqual(resultado, "Holobit H1 liberado.")

    def test_execute_instruction_allocate(self):
        """ Prueba la ejecución de una instrucción ensamblador para asignar un Holobit. """
        resultado = self.executor.ejecutar_instruccion("ALLOCATE H2 0.4 0.5 0.6")
        self.assertEqual(resultado, "Holobit H2 asignado en (0.4, 0.5, 0.6).")

    def test_execute_instruction_get_position(self):
        """ Prueba la ejecución de una instrucción ensamblador para obtener la posición de un Holobit. """
        self.executor.ejecutar_instruccion("ALLOCATE H3 0.7 0.8 0.9")
        resultado = self.executor.ejecutar_instruccion("GET_POSITION H3")
        self.assertEqual(resultado, "Posición de H3: (0.7, 0.8, 0.9)")

    def test_execute_instruction_deallocate(self):
        """ Prueba la ejecución de una instrucción ensamblador para liberar un Holobit. """
        self.executor.ejecutar_instruccion("ALLOCATE H4 1.0 1.1 1.2")
        resultado = self.executor.ejecutar_instruccion("DEALLOCATE H4")
        self.assertEqual(resultado, "Holobit H4 liberado.")


if __name__ == "__main__":
    unittest.main()