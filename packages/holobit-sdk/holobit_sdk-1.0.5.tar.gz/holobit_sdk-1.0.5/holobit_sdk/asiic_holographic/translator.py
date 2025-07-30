class ASIICTranslator:
    """
    Traductor del ASIIC Holográfico a lenguaje ensamblador holográfico.
    """

    def __init__(self):
        self.mapeo_instrucciones = {
            "ROTAR": "ROT",
            "ENTRELAZAR": "ENTR"
        }

    def traducir(self, comando):
        """
        Convierte un comando ASIIC en su equivalente en lenguaje ensamblador holográfico.

        Args:
            comando (str): Comando ASIIC a traducir.

        Returns:
            str: Comando traducido al ensamblador holográfico.
        """
        partes = comando.split()
        if not partes:
            return "Comando vacío"

        nombre = partes[0]
        argumentos = " ".join(partes[1:])

        if nombre in self.mapeo_instrucciones:
            return f"{self.mapeo_instrucciones[nombre]} {argumentos}"
        else:
            return f"Instrucción desconocida: {nombre}"


# Ejemplo de uso
if __name__ == "__main__":
    traductor = ASIICTranslator()

    # Pruebas de traducción
    print(traductor.traducir("ROTAR H1 z 90"))  # Debe devolver "ROT H1 z 90"
    print(traductor.traducir("ENTRELAZAR H1 H2"))  # Debe devolver "ENTR H1 H2"
    print(traductor.traducir("DESCONOCIDO X Y Z"))  # Debe devolver "Instrucción desconocida: DESCONOCIDO"
