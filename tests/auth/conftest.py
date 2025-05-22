
import pytest
from src.auth_service import obtener_token

@pytest.fixture
def token_valido(usuario_admin):
    """Obtiene un token válido para autenticación."""
    usuario = usuario_admin["usuario"]
    password = usuario_admin["password"]
    token = obtener_token(usuario, password)
    return token

@pytest.fixture
def var_raiz():    
    return "auth"

