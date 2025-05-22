
import pytest

@pytest.fixture
def datos_pago():
    """Datos para el pago bancario."""
    return {
        "monto": 1000,
        "cuenta_destino": "1234567890"
    }

@pytest.fixture
def var_raiz():    
    return "payments"