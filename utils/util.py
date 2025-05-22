from datetime import datetime, timedelta
import json
from pathlib import Path
from jsonschema import ValidationError, validate
import pytest
import os
import re

def validar_schema(response_json, nombre_schema):
    """Valida el response_json contra el esquema con el nombre especificado."""
    
    def cargar_schema(nombre_schema: str) -> dict:
        """Cargar el esquema desde el archivo JSON según el nombre proporcionado."""
        schema_file_path = Path(__file__).resolve().parent.parent / 'data' / 'schema.json'
    
        with open(schema_file_path) as schema_file:
            schemas = json.load(schema_file)
        
        # Verifica que el nombre del esquema exista en el JSON
        if nombre_schema not in schemas:
            raise KeyError(f"Esquema '{nombre_schema}' no encontrado.")
        
        return schemas[nombre_schema]
    
    schema = cargar_schema(nombre_schema)
    
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Error de validación: {e.message}")

    assert True, "El esquema es válido."

#Formatea la fecha del response -3 horas, para validarlo con la base de datos
def format_response_date(fecha_response):
    fecha_response_dt = datetime.strptime(fecha_response, "%Y-%m-%dT%H:%M:%S.%fZ")
    return (fecha_response_dt - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S.%f")
    
def assert_payment_data(response, db_data):
    assert db_data is not None, "Error: No se encontraron datos en la base de datos"
    assert bool(db_data), "Error: Los datos obtenidos de la base de datos están vacíos."

    fecha_response = format_response_date(response["transaction"]["datetime"]) 
    assert fecha_response == db_data["fecha_formateada"], f"Falla la validacion de fecha: {fecha_response} != {db_data['fecha_formateada']}"
    assert response["transaction"]["code"] == db_data["estado_cod"], "Falla la validacion de estado_cod"
    assert response["transaction"]["code"] == db_data["estado_trx_a_cod"] or db_data["estado_trx_a_cod"] is None, "Falla la validacion de estado_trx_a_cod"
    assert response["transaction"]["code"] == db_data["estado_trx_b_cod"] or db_data["estado_trx_b_cod"] is None, "Falla la validacion de estado_trx_b_cod"
    assert response["qr_id"] == db_data["qr_id"], "Falla la validacion de qr_id"
    assert response["transaction"]["authorization_code"] == db_data["authorization_code"], "Falla la validacion de authorization_code"
    assert response["transaction"]["gross_amount"]["value"] == db_data["importe_bruto"], "Falla la validacion de importe_bruto"

def assert_pagos_data(response, db_data):
    assert db_data is not None, "Error: No se encontraron datos en la base de datos"
    assert bool(db_data), "Error: Los datos obtenidos de la base de datos están vacíos."

    fecha_response = format_response_date(response["transaccion"]["fecha"]) 
    assert fecha_response == db_data["fecha_formateada"], f"Falla la validacion de fecha: {fecha_response} != {db_data['fecha_formateada']}"
    assert response["transaccion"]["codigo"] == db_data["estado_cod"], "Falla la validacion de estado_cod"
    assert response["transaccion"]["codigo"] == db_data["estado_trx_a_cod"] or db_data["estado_trx_a_cod"] is None, "Falla la validacion de estado_trx_a_cod"
    assert response["transaccion"]["codigo"] == db_data["estado_trx_b_cod"] or db_data["estado_trx_b_cod"] is None, "Falla la validacion de estado_trx_b_cod"
    assert response["qrId"] == db_data["qr_id"], "Falla la validacion de qr_id"
    assert response["transaccion"]["authorizationCode"] == db_data["authorization_code"], "Falla la validacion de authorization_code"
    assert response["transaccion"]["montoBruto"]["valor"] == db_data["importe_bruto"], "Falla la validacion de importe_bruto"

def validar_comisiones(db_data, comision_prov_cta, comision_acpt, comision_admin, categoria, retencion, net_amount):
    assert db_data["prov_cta_importe_comision"] == comision_prov_cta, f"La comisión de billetera no coincide para {categoria}"
    assert db_data["acpt_importe_comision"] == comision_acpt, f"La comisión del aceptador no coincide para {categoria}"
    assert db_data["adm_importe_comision"] == comision_admin, f"La comisión del administrador no coincide para {categoria}"
    assert db_data["comercio_categoria_cod"] == categoria, f"No coincide la categoría del comercio: {categoria}"

    total_comisiones = comision_prov_cta + comision_admin + comision_acpt
    neto_a_recibir = 1000 - total_comisiones - retencion
    assert neto_a_recibir == net_amount, "El neto a recibir no coincide"


def load_json_with_config(file_path):
    """
    Carga un archivo JSON y reemplaza las variables usando el objeto global `config`.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        json_content = file.read()  # Leer archivo como string

    # Función que busca y reemplaza las variables con `config`
    def replace_var(match):
        keys = match.group(1).split(".")  # Divide "config.dato" en ["config", "dato"]
        value = config  # Empezamos con el objeto global
        
        # Navegar en el diccionario usando los nombres de las claves
        for key in keys[1:]:  # Omitimos "config", ya que es nuestro objeto base
            value = value.get(key, f"#{match.group(1)}")  # Obtener valor o dejar la variable sin reemplazar
        return str(value)

    # Reemplazo con regex buscando `#(config.algo)`
    json_string = re.sub(r"#\((config\.[\w.]+)\)", replace_var, json_content)

    return json.loads(json_string)  # Convertimos a diccionario Python


VALID_ENVIRONMENTS = {"dev", "homo", "prod"}

class DotDict(dict):
    """Permite acceder a los elementos de un diccionario con notación de punto."""
    def __getattr__(self, key):
        value = self.get(key)
        if isinstance(value, dict):  # Convierte los diccionarios en DotDict
            return DotDict(value)
        return value

def load_config():
    env = os.getenv("ENV", "homo")


    if env not in VALID_ENVIRONMENTS:
        raise ValueError(f"ENV debe ser uno de {VALID_ENVIRONMENTS}, pero se recibió '{env}'")

    config_path = f"data/data_{env}.json"

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return DotDict(data)

# Cargar configuración
config = load_config()