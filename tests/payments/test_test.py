import json
import os
import random
import string

from jsonschema import validate
import pytest
from utils.util import config, load_json_with_config


path_pull = os.path.join(os.path.dirname(__file__), 'data/request_pagos.json')

request_data = load_json_with_config(path_pull)
    
   
#@pytest.mark.parametrize("request_data", ["alta_pago.json"], indirect=True)
def test_cambios_conftest(var_raiz):
    client_id = config.clientes.aceptadores.cuenta
    assert client_id == "342rerte344-rerw-535-54re-r435ewr"
    print("El valor fixture de var_raiz es: ", var_raiz)
    print("El URL del pago es: ", config.environment_config.url_base)
    print("El client_id es: ", client_id)
    print("El request es: ", request_data)

