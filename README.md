
# PyTest Example

ejemplo con múltiples archivos `conftest.py` en PyTest para manejar dominios separados:

### Estructura del Proyecto:
```
pago_conftest/
├── src/
│   ├── auth_service.py
│   └── payment_service.py
│
├── tests/
│   ├── auth/
│   │   ├── conftest.py
│   │   └── test_auth.py
│   │
│   ├── payments/
│   │   ├── conftest.py
│   │   └── test_payments.py
│   │
│   └── conftest.py
│
└── README.md
```

### Explicación de los conftest:
1. **conftest.py (raíz)**:
   - Define un usuario administrador y sus credenciales.
   - Tiene un fixture igual al de conftest de auth
   - Se comparte entre todos los tests del proyecto.

2. **conftest.py (auth)**:
   - Genera un token válido usando el usuario del conftest raíz.
   - Es exclusivo para los tests de autenticación.

3. **conftest.py (payments)**:
   - Define datos específicos para los pagos.
   - Es exclusivo para los tests de pago.


# Resumen clave:

Local primero: PyTest siempre busca en el conftest.py más cercano.

Ascendente: Si no lo encuentra, sube de nivel.

No cruza dominios: No busca en carpetas hermanas (auth no ve payments y viceversa).

Conftest raíz: Si está en la raíz, es accesible para todos.


### Comandos para ejecutar:
Para ejecutar todos los tests: -s para que muestre los print
```
pytest -v -s
```
Para ejecutar solo los tests de autenticación:
```
pytest tests/auth -v
```
Para ejecutar solo los tests de pagos:
```
pytest tests/payments -v
```
