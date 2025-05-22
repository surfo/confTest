
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

@pytest.fixture
def datos_devolucion(request):
    """Fixture que recibe parámetros desde el test."""
    params = request.param 
    # Simula modificación para mostrar que pasó por acá
    params["id_wallet"] = f"{params['id_wallet']}_modificado"
    params["codigo_comercio"] = params["codigo_comercio"].lower()
    # Aquí podrías incluir lógica adicional, como validaciones o transformaciones
    return params