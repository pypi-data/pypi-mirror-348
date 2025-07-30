# Archivo: multi_level/high_level/compiler.py

from multi_level.high_level.hololang_parser import HoloLangParser
from multi_level.low_level.execution_unit import ExecutionUnit
from transpiler.machine_code_transpiler import MachineCodeTranspiler

class HoloLangCompiler:
    """
    Compilador para el lenguaje de programación holográfico, ahora integrado con el transpilador.
    """

    def __init__(self, architecture="x86"):
        self.parser = HoloLangParser()
        self.executor = ExecutionUnit()
        self.transpiler = MachineCodeTranspiler(architecture)

    def compilar_y_ejecutar(self, codigo):
        """
        Compila y ejecuta una línea de código en HoloLang.

        Args:
            codigo (str): Código fuente en HoloLang.

        Returns:
            str: Resultado de la ejecución del código compilado o código máquina generado.
        """
        resultado = self.parser.interpretar(codigo)

        if "Variable" in resultado:
            return resultado  # La variable se ha creado correctamente

        if "IMPRIMIR" in codigo:
            return resultado  # Devolvemos la impresión

        # Si se trata de una operación, convertirla a código máquina con el transpilador
        partes = codigo.split()
        if partes[0] == "EJECUTAR":
            instruccion = " ".join(partes[1:])
            codigo_maquina = self.transpiler.transpile(instruccion)
            return f"Código máquina generado: {codigo_maquina}"

        return "Error: Comando no reconocido."


# Ejemplo de uso
if __name__ == "__main__":
    compiler = HoloLangCompiler("x86")
    print(compiler.compilar_y_ejecutar("CREAR H1 (0.1, 0.2, 0.3)"))
    print(compiler.compilar_y_ejecutar("IMPRIMIR H1"))
    print(compiler.compilar_y_ejecutar("EJECUTAR MULT H1 H2"))  # Ahora genera código máquina
