from configparser import ConfigParser


def _get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    key = config["openweather"]["api_key"]
    return key


_get_api_key()

"""
° A linha 3 importa o ConfigParser do módulo configparser do Python.

° A linha 5 define _get_api_key(), iniciando o nome com um caractere sublinhado (_). 
  Essa convenção de nomenclatura indica que a função deve ser considerada não pública.

° As linhas 6 a 12 compõem uma docstring para a função.

° A linha 13 instancia um objeto ConfigParser que você nomeou config.

° A linha 14 usa .read() para carregar as informações que você salvou em secrets.ini em seu script Python.

° A linha 15 retorna o valor de sua chave de API acessando o valor do dicionário usando a notação de colchetes.
"""
