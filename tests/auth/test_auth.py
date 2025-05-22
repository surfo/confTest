import pytest



def test_obtener_token(token_valido, var_raiz):
    print("\n[INFO]Token válido:", token_valido)
    print("\n[INFO]Variable del conftest compartida con auth y raiz:", var_raiz)
    assert token_valido == "token_valido_123"
