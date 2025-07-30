import re
import ast


class HoloLangParser:
    """
    Analizador sintáctico para el lenguaje de programación holográfico.
    """

    def __init__(self):
        self.variables = {}

    def interpretar(self, codigo):
        """
        Interpreta una línea de código en HoloLang.

        Args:
            codigo (str): Línea de código en HoloLang.

        Returns:
            str: Resultado de la ejecución de la línea de código.
        """
        codigo = codigo.strip()

        if re.match(r'CREAR\s+\w+\s+\(.*\)', codigo):
            return self._crear_variable(codigo)
        elif re.match(r'IMPRIMIR\s+\w+', codigo):
            return self._imprimir_variable(codigo)
        else:
            return "Error de sintaxis."

    def _crear_variable(self, codigo):
        """
        Crea una variable en HoloLang.

        Args:
            codigo (str): Línea de código que define la variable.

        Returns:
            str: Confirmación de la creación de la variable.
        """
        partes = re.findall(r'\w+', codigo)
        nombre = partes[1]

        # Extrae correctamente los valores entre paréntesis
        valores_match = re.search(r'\((.*?)\)', codigo)
        if valores_match:
            valores = tuple(map(float, valores_match.group(1).split(',')))
            self.variables[nombre] = valores
            return f"Variable {nombre} creada con valores {valores}"

        return "Error de sintaxis en la declaración de la variable."

    def _imprimir_variable(self, codigo):
        """
        Imprime el valor de una variable en HoloLang.

        Args:
            codigo (str): Línea de código que solicita la impresión.

        Returns:
            str: Valor de la variable o mensaje de error.
        """
        nombre = codigo.split()[1]
        if nombre in self.variables:
            return f"{nombre} = {self.variables[nombre]}"
        return f"Error: Variable {nombre} no definida."


# Ejemplo de uso
if __name__ == "__main__":
    parser = HoloLangParser()
    print(parser.interpretar("CREAR H1 (0.1, 0.2, 0.3)"))
    print(parser.interpretar("IMPRIMIR H1"))
