import pytest
from transpiler.machine_code_transpiler import MachineCodeTranspiler

@pytest.fixture
def transpiler():
    return MachineCodeTranspiler()

def test_transpile_allocate(transpiler):
    result = transpiler.transpile("ALLOCATE H1 0.1 0.2 0.3")
    assert result == "MOV H1 0.1 0.2 0.3"

def test_transpile_deallocate(transpiler):
    result = transpiler.transpile("DEALLOCATE H1")
    assert result == "FREE H1"

def test_transpile_get_position(transpiler):
    result = transpiler.transpile("GET_POSITION H1")
    assert result == "READ_POS H1"

def test_transpile_rotate(transpiler):
    result = transpiler.transpile("ROTATE H1 z 90")
    assert result == "ROT H1 z 90"

def test_transpile_unknown_instruction(transpiler):
    result = transpiler.transpile("UNKNOWN_CMD H1")
    assert result == "Instrucción holográfica desconocida: UNKNOWN_CMD"
