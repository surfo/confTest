
from src.payment_service import procesar_pago

def test_procesar_pago(token_valido, datos_pago):
    resultado = procesar_pago(token_valido, datos_pago["monto"], datos_pago["cuenta_destino"])
    assert resultado["status"] == "aprobado"
    assert resultado["cuenta"] == datos_pago["cuenta_destino"]
    assert resultado["monto"] == datos_pago["monto"]

def test_procesar_pago_fallido():
    resultado = procesar_pago("token_invalido", 1000, "1234567890")
    assert resultado["status"] == "rechazado"
    assert resultado["motivo"] == "Token inválido o monto incorrecto"
