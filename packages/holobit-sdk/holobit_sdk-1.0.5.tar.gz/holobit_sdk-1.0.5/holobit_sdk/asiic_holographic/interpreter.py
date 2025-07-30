from asiic_holographic.instructions import ASIICInstructions


class ASIICInterpreter:
    """
    Intérprete del ASIIC Holográfico.
    """

    def __init__(self):
        self.instrucciones = ASIICInstructions()
        self._cargar_instrucciones()

    def _cargar_instrucciones(self):
        """
        Registra las instrucciones básicas del ASIIC Holográfico.
        """

        def rotar(holobit, eje, angulo):
            return f"Rotando Holobit {holobit} en el eje {eje} con {angulo} grados"

        def entrelazar(holobit1, holobit2):
            return f"Entrelazando Holobits {holobit1} y {holobit2}"

        self.instrucciones.agregar_instruccion("ROTAR", rotar)
        self.instrucciones.agregar_instruccion("ENTRELAZAR", entrelazar)

    def interpretar(self, comando):
        """
        Procesa un comando en lenguaje ASIIC y ejecuta la instrucción correspondiente.

        Args:
            comando (str): Comando ASIIC a interpretar.

        Returns:
            str: Resultado de la ejecución del comando.
        """
        partes = comando.split()
        if not partes:
            return "Comando vacío"

        nombre = partes[0]
        argumentos = partes[1:]

        try:
            return self.instrucciones.ejecutar_instruccion(nombre, *argumentos)
        except ValueError as e:
            return str(e)


# Ejemplo de uso
if __name__ == "__main__":
    interprete = ASIICInterpreter()

    # Ejecutar comandos de prueba
    print(interprete.interpretar("ROTAR H1 z 90"))
    print(interprete.interpretar("ENTRELAZAR H1 H2"))