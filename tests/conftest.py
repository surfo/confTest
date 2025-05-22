
import pytest
from src.auth_service import obtener_token

@pytest.fixture(scope="session")
def usuario_admin():
    """Simula un usuario administrador."""
    return {"usuario": "admin", "password": "1234"}

@pytest.fixture
def token_valido(usuario_admin):
    """Obtiene un token válido para autenticación."""
    usuario = usuario_admin["usuario"]
    password = usuario_admin["password"]
    token = obtener_token(usuario, password)
    return token

@pytest.fixture
def var_raiz():    
    return "raiz"

@pytest.fixture
def datos_devolucion(request):
    """Fixture que recibe parámetros desde el test."""
    parametros = request.param
    # Aquí podrías incluir lógica adicional, como validaciones o transformaciones
    return parametros