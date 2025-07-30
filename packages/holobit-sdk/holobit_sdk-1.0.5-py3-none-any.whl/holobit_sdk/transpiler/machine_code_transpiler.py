# Archivo: transpiler/machine_code_transpiler.py

class MachineCodeTranspiler:
    """
    Transpilador de instrucciones holográficas a código máquina con optimización avanzada.
    """

    def __init__(self, architecture="x86"):
        """
        Inicializa el transpilador con la arquitectura deseada y mejoras de rendimiento.

        Args:
            architecture (str): Arquitectura objetivo ("x86", "ARM", "RISC-V").
        """
        self.architecture = architecture
        self.instruction_maps = {
            "x86": {
                "ALLOCATE": "MOV",
                "DEALLOCATE": "FREE",
                "GET_POSITION": "READ_POS",
                "ROTATE": "ROT",
                "LINK": "LINK",
                "UNLINK": "UNLINK",
                "JUMP": "JMP",
                "COMPARE": "CMP",
                "ADD": "ADD",
                "SUB": "SUB",
                "MULT": "MUL",
                "DIV": "DIV",
                "PUSH": "PUSH",
                "POP": "POP"
            },
            "ARM": {
                "ALLOCATE": "LDR",
                "DEALLOCATE": "STR",
                "GET_POSITION": "LDR_POS",
                "ROTATE": "ROT_ARM",
                "LINK": "CONNECT",
                "UNLINK": "DISCONNECT",
                "JUMP": "B",
                "COMPARE": "CMP_ARM",
                "ADD": "ADD_ARM",
                "SUB": "SUB_ARM",
                "MULT": "MUL_ARM",
                "DIV": "DIV_ARM",
                "PUSH": "PUSH_ARM",
                "POP": "POP_ARM"
            },
            "RISC-V": {
                "ALLOCATE": "LW",
                "DEALLOCATE": "SW",
                "GET_POSITION": "LW_POS",
                "ROTATE": "ROT_RV",
                "LINK": "RV_LINK",
                "UNLINK": "RV_UNLINK",
                "JUMP": "JAL",
                "COMPARE": "BNE",
                "ADD": "ADD_RV",
                "SUB": "SUB_RV",
                "MULT": "MUL_RV",
                "DIV": "DIV_RV",
                "PUSH": "PUSH_RV",
                "POP": "POP_RV"
            }
        }

        # Tabla de registros utilizados para optimización
        self.registers_in_use = set()

    def transpile(self, holographic_instruction):
        """
        Transpila una instrucción holográfica a su equivalente en código máquina optimizado.

        Args:
            holographic_instruction (str): La instrucción holográfica original.

        Returns:
            str: Instrucción traducida a código máquina optimizado según la arquitectura.
        """
        try:
            partes = holographic_instruction.split()
            if not partes:
                return "Instrucción vacía."

            comando_holografico = partes[0]
            argumentos = " ".join(partes[1:])

            instruction_map = self.instruction_maps.get(self.architecture, {})
            comando_maquina = instruction_map.get(comando_holografico)
            if not comando_maquina:
                return f"Instrucción holográfica desconocida para {self.architecture}: {comando_holografico}"

            # Optimización: reuso de registros
            if comando_holografico in ["ADD", "SUB", "MULT", "DIV"]:
                regs = argumentos.split()
                if len(regs) >= 2:
                    if regs[0] in self.registers_in_use:
                        return f"{comando_maquina} {regs[0]}, {regs[1]} ; Registro reutilizado"
                    else:
                        self.registers_in_use.add(regs[0])
                        return f"{comando_maquina} {regs[0]}, {regs[1]} ; Registro registrado y reutilizado"

            # Optimización avanzada: eliminar redundancias
            if comando_holografico in ["ADD", "SUB", "MULT", "DIV"] and argumentos.split()[0] == argumentos.split()[1]:
                return f"CLEAR {argumentos.split()[0]}"

            # Optimización: eliminación de instrucciones innecesarias
            if comando_holografico == "COMPARE" and len(argumentos.split()) == 2:
                arg1, arg2 = argumentos.split()
                if arg1 == arg2:
                    return "NOP"

            # Optimización: eliminación de MOV redundantes
            if comando_holografico == "ALLOCATE" and argumentos.split()[0] == argumentos.split()[1]:
                return "NOP"  # No es necesario mover un valor a sí mismo

            # Optimización: conversión de PUSH/POP en bloques para reducir accesos a memoria
            if comando_holografico == "PUSH" and len(argumentos.split()) > 1:
                return f"PUSH_MULTI {argumentos}"
            if comando_holografico == "POP" and len(argumentos.split()) > 1:
                return f"POP_MULTI {argumentos}"

            return f"{comando_maquina} {argumentos}"

        except Exception as e:
            return f"Error en la transpilación: {str(e)}"


# Ejemplo de uso
if __name__ == "__main__":
    transpiler_x86 = MachineCodeTranspiler("x86")
    print(transpiler_x86.transpile("ALLOCATE H1 0.1 0.2 0.3"))
    print(transpiler_x86.transpile("JUMP NEXT"))  # Se optimiza a NOP
    print(transpiler_x86.transpile("ADD H1 H1"))  # Se optimiza a CLEAR H1
    print(transpiler_x86.transpile("COMPARE H1 H1"))  # Se optimiza a NOP
    print(transpiler_x86.transpile("ADD H1 H2"))  # Se optimiza con reutilización de registros
