import numpy as np


class MemoryManager:
    """
    Administrador de memoria holográfica para la gestión de Holobits.
    """

    def __init__(self, size=1024):
        """
        Inicializa la memoria holográfica.

        Args:
            size (int): Cantidad máxima de Holobits que pueden almacenarse.
        """
        self.size = size
        self.memory = np.zeros((size, 3))  # Representación tridimensional de Holobits
        self.allocated = {}

    def allocate(self, holobit_id, position):
        """
        Asigna un Holobit a una posición específica en la memoria.

        Args:
            holobit_id (str): Identificador único del Holobit.
            position (tuple): Coordenadas en el espacio holográfico (x, y, z).
        """
        if holobit_id in self.allocated:
            raise ValueError(f"El Holobit {holobit_id} ya está asignado.")

        index = len(self.allocated)
        if index >= self.size:
            raise MemoryError("Memoria holográfica llena.")

        self.memory[index] = position
        self.allocated[holobit_id] = index

    def deallocate(self, holobit_id):
        """
        Libera la memoria ocupada por un Holobit.

        Args:
            holobit_id (str): Identificador del Holobit a liberar.
        """
        if holobit_id not in self.allocated:
            raise KeyError(f"El Holobit {holobit_id} no está en la memoria.")

        index = self.allocated.pop(holobit_id)
        self.memory[index] = np.zeros(3)

    def get_position(self, holobit_id):
        """
        Obtiene la posición actual de un Holobit en la memoria.

        Args:
            holobit_id (str): Identificador del Holobit.

        Returns:
            tuple: Coordenadas (x, y, z) del Holobit.
        """
        if holobit_id not in self.allocated:
            raise KeyError(f"El Holobit {holobit_id} no está en la memoria.")

        index = self.allocated[holobit_id]
        return tuple(map(float, self.memory[index]))


# Ejemplo de uso
if __name__ == "__main__":
    mem_manager = MemoryManager()
    mem_manager.allocate("H1", (0.1, 0.2, 0.3))
    print("Posición de H1:", mem_manager.get_position("H1"))
    mem_manager.deallocate("H1")
