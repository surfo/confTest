
def procesar_pago(token, monto, cuenta_destino):
    if token == "token_valido_123" and monto > 0:
        return {
            "status": "aprobado",
            "cuenta": cuenta_destino,
            "monto": monto
        }
    else:
        return {
            "status": "rechazado",
            "motivo": "Token inválido o monto incorrecto"
        }
