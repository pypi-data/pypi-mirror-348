from multi_level.low_level.low_level_api import LowLevelAPI


class HolographicAPI:
    """
    API de Nivel Medio para la manipulación de Holobits en un entorno cuántico-holográfico.
    """

    def __init__(self):
        self.low_level_api = LowLevelAPI()

    def crear_holobit(self, holobit_id, x, y, z):
        """
        Crea un nuevo Holobit en la memoria holográfica.

        Args:
            holobit_id (str): Identificador único del Holobit.
            x (float): Coordenada X.
            y (float): Coordenada Y.
            z (float): Coordenada Z.

        Returns:
            str: Mensaje de confirmación.
        """
        return self.low_level_api.ejecutar_comando("ALLOCATE", holobit_id, x, y, z)

    def obtener_posicion(self, holobit_id):
        """
        Obtiene la posición de un Holobit en el espacio holográfico.

        Args:
            holobit_id (str): Identificador del Holobit.

        Returns:
            str: Coordenadas del Holobit.
        """
        return self.low_level_api.ejecutar_comando("GET_POSITION", holobit_id)

    def eliminar_holobit(self, holobit_id):
        """
        Elimina un Holobit de la memoria holográfica.

        Args:
            holobit_id (str): Identificador del Holobit.

        Returns:
            str: Mensaje de confirmación.
        """
        return self.low_level_api.ejecutar_comando("DEALLOCATE", holobit_id)


# Ejemplo de uso
if __name__ == "__main__":
    api = HolographicAPI()
    print(api.crear_holobit("H1", 0.1, 0.2, 0.3))
    print(api.obtener_posicion("H1"))
    print(api.eliminar_holobit("H1"))
