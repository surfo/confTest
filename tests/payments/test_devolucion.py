# tests/test_devolucion.py

import pytest

@pytest.mark.parametrize(
    "datos_devolucion",
    [
        {"id_wallet": "WALLET123", "codigo_comercio": "COM001"},
        {"id_wallet": "WALLET456", "codigo_comercio": "COM002"},
    ],
    indirect=True
)
def test_procesar_devolucion(datos_devolucion):
    """Test que utiliza la fixture parametrizada."""
    id_wallet = datos_devolucion["id_wallet"]
    codigo_comercio = datos_devolucion["codigo_comercio"]
    
    # Simulación de lógica de devolución
    print(f"Procesando devolución para wallet {id_wallet} y comercio {codigo_comercio}")
    # Aquí iría la lógica real del test, como llamadas a la API y aserciones
