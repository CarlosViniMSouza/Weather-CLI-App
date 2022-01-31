from urllib import error, parse, request
from configparser import ConfigParser
from pprint import pp
import argparse
import json
import sys


# A linha de código abaixo fará todas as chamadas de API constantemente
URL = "http://api.openweathermap.org/data/2.5/weather"

PAD = 20

REVERSE = ["\033[;42m", "\033[;45m", "\033[;33m"]

RESET = "\033[0m"


def _get_api_key():
    config = ConfigParser()

    config.read("secrets.ini")

    return config["openweather"]["api_key"]


def read_user_cli_args():
    parser = argparse.ArgumentParser(description="inform weather for a city")

    parser.add_argument("city", nargs="+", type=str, help="Insert the city name")

    parser.add_argument("-i", "--imperial", action="store_true", help="Temp. in imperial units")

    return parser.parse_args()


"""
Teste no terminal a aplicação, irá aparecer a seguinte mensagem de erro:

usage: weather.py [-h]
weather.py: error: unrecognized arguments: vienna

O Python primeiro imprime informações de uso em seu console. Essas informações sugerem a ajuda interna (-h) fornecida pelo ArgumentParser. 
Em seguida, ele informa que seu analisador não reconheceu o argumento que você passou para o programa usando sua CLI.
"""


"""
No entanto, se você executar o script e passar um nome de cidade como entrada, ainda não poderá ver nenhuma saída exibida de volta ao seu console. 
Volte para weather.py e edite o código em seu bloco de código condicional na parte inferior do arquivo:
"""


def build_query(city_input, imperial=False):
    api_key = _get_api_key()

    city_name = " ".join(city_input)

    url_encoded_city_name = parse.quote_plus(city_name)

    units = "imperial" if imperial else "metric"

    url = (
        f"{URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )

    return url


"""
Você começou adicionando uma nova instrução de importação na linha 5. Você usará uma função do módulo urllib.parse
na linha 24 para ajudar a limpar a entrada do usuário para que a API possa consumi-la com segurança.
"""


def get_data(query_url):
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:
            sys.exit("ACCESS DENIED!")
        elif http_error.code == 404:
            sys.exit("Weather Data Inexist!")
        else:
            sys.exit(f"Something went strange ... ({http_error.code})")

    data = response.read()

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Ineligible answer!")


def display_info(weather_data, imperial=False):
    city = weather_data["name"]

    weather_description = weather_data["weather"][0]["description"]

    temperature = weather_data["main"]["temp"]

    print(f"{REVERSE[0]}{city:^{PAD}}{RESET}", end="")
    print(f"\t{REVERSE[1]}{weather_description.capitalize():^{PAD}}{RESET}", end=" ")
    print(f"{REVERSE[2]}({temperature}°{'F' if imperial else 'C'}){RESET}")


"""
Nota: Com essas adições, você tornou seu aplicativo de previsão do tempo Python mais fácil de usar para desenvolvedores e não desenvolvedores!
"""


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_query(user_args.city, user_args.imperial)
    weather_data = get_data(query_url)
    display_info(weather_data, user_args.imperial)
