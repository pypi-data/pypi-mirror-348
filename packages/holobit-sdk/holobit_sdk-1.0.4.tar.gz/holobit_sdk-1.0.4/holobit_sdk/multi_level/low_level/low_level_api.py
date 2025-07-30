from multi_level.low_level.memory_manager import MemoryManager


class LowLevelAPI:
    """
    API de Bajo Nivel para interactuar con el Ensamblador Cuántico Holográfico.
    """

    def __init__(self):
        self.memory = MemoryManager()

    def ejecutar_comando(self, comando, *args):
        """
        Ejecuta un comando ensamblador de bajo nivel.

        Args:
            comando (str): Nombre del comando a ejecutar.
            *args: Argumentos adicionales según el comando.

        Returns:
            str: Resultado de la ejecución del comando.
        """
        if comando == "ALLOCATE":
            holobit_id, x, y, z = args
            self.memory.allocate(holobit_id, (float(x), float(y), float(z)))
            return f"Holobit {holobit_id} asignado en ({x}, {y}, {z})."

        elif comando == "DEALLOCATE":
            holobit_id = args[0]
            self.memory.deallocate(holobit_id)
            return f"Holobit {holobit_id} liberado."

        elif comando == "GET_POSITION":
            holobit_id = args[0]
            position = self.memory.get_position(holobit_id)
            return f"Posición de {holobit_id}: {position}"

        else:
            return "Comando desconocido."


# Ejemplo de uso
if __name__ == "__main__":
    api = LowLevelAPI()
    print(api.ejecutar_comando("ALLOCATE", "H1", 0.1, 0.2, 0.3))
    print(api.ejecutar_comando("GET_POSITION", "H1"))
    print(api.ejecutar_comando("DEALLOCATE", "H1"))
