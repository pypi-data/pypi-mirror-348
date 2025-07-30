import numpy as np


class VectorProcessor:
    """
    Procesador de operaciones vectoriales para Holobits en el entorno cuántico-holográfico.
    """

    @staticmethod
    def suma_vectores(v1, v2):
        """
        Suma dos vectores tridimensionales.

        Args:
            v1 (tuple): Primer vector (x, y, z).
            v2 (tuple): Segundo vector (x, y, z).

        Returns:
            tuple: Resultado de la suma.
        """
        return tuple(np.add(v1, v2))

    @staticmethod
    def producto_escalar(v1, v2):
        """
        Calcula el producto escalar entre dos vectores tridimensionales.

        Args:
            v1 (tuple): Primer vector (x, y, z).
            v2 (tuple): Segundo vector (x, y, z).

        Returns:
            float: Resultado del producto escalar.
        """
        return float(np.dot(v1, v2))

    @staticmethod
    def norma_vector(v):
        """
        Calcula la norma de un vector tridimensional.

        Args:
            v (tuple): Vector (x, y, z).

        Returns:
            float: Norma del vector.
        """
        return float(np.linalg.norm(v))


# Ejemplo de uso
if __name__ == "__main__":
    v1 = (1.0, 2.0, 3.0)
    v2 = (4.0, 5.0, 6.0)

    print("Suma de vectores:", VectorProcessor.suma_vectores(v1, v2))
    print("Producto escalar:", VectorProcessor.producto_escalar(v1, v2))
    print("Norma del vector v1:", VectorProcessor.norma_vector(v1))
