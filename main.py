from urllib import error, parse, request
from configparser import ConfigParser
from pprint import pp
import argparse
import style
import json
import sys


# A linha de código abaixo fará todas as chamadas de API constantemente
URL = "http://api.openweathermap.org/data/2.5/weather"


"""
Semelhante aos códigos de resposta HTTP, a API de clima fornece um código de condição climática com cada resposta. 
Esse código categoriza as condições climáticas em grupos definidos por um intervalo de números de identificação.
"""

THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


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

    weather_id = weather_data["weather"][0]["id"]

    weather_description = weather_data["weather"][0]["description"]

    temperature = weather_data["main"]["temp"]

    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)

    weather_symbol, color = _select_weather_display_params(weather_id)

    style.change_color(color)
    print(f"\t{weather_symbol}", end=" ")
    print(f"{weather_description.capitalize():^{style.PADDING}}", end=" ")
    style.change_color(style.RESET)

    print(f"({temperature}°{'F' if imperial else 'C'})")


def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("💥", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("🔆", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", style.WHITE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", style.RESET)
    return display_params


"""
Com esta atualização, você adicionou um emoji a cada ID de clima 
e resumiu os dois parâmetros de exibição em uma tupla.
"""

"""
Nota: Com essas adições, você tornou seu aplicativo de previsão do tempo Python 
mais fácil de usar para desenvolvedores e não desenvolvedores!
"""


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_query(user_args.city, user_args.imperial)
    weather_data = get_data(query_url)
    display_info(weather_data, user_args.imperial)

"""
Com esta última alteração configurada em seu aplicativo de clima Python, você terminou de criar sua ferramenta CLI. 
Agora você pode acessar seu mecanismo de busca favorito, procurar alguns nomes divertidos de cidades e passar o resto deste dia chuvoso 
procurando um lugar onde você possa sonhar em passar suas próximas férias.
"""
