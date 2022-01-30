from configparser import ConfigParser
import argparse
import env


def _get_api_key():
    config = ConfigParser()

    config.read("secrets.ini")

    return config["openweather"]["api_key"]


"""
° A linha 3 importa o ConfigParser do módulo configparser do Python.

° A linha 5 define _get_api_key(), iniciando o nome com um caractere sublinhado (_). 
  Essa convenção de nomenclatura indica que a função deve ser considerada não pública.

° As linhas 6 a 12 compõem uma docstring para a função.

° A linha 13 instancia um objeto ConfigParser que você nomeou config.

° A linha 14 usa .read() para carregar as informações que você salvou em secrets.ini em seu script Python.

° A linha 15 retorna o valor de sua chave de API acessando o valor do dicionário usando a notação de colchetes.
"""


def read_user_cli_args():
    parser = argparse.ArgumentParser(description="inform weather for a city")

    parser.add_argument("city", nargs="+", type=str, help="Insert the city name")

    parser.add_argument("-i", "--imperial", action="store_true", help="Temp. in imperial units")

    return parser.parse_args()


"""
° As linhas 12 a 14 criam uma instância de argparse.ArgumentParser, para a qual você passa uma descrição opcional do analisador na linha 13.

° A linha 15 retorna os resultados de uma chamada para .parse_args(), que eventualmente serão os valores de entrada do usuário.

° A linha 19 abre um bloco condicional após verificar o namespace "__main__" do Python,
que permite definir o código que deve ser executado quando você estiver executando weather.py como um script.

° A linha 20 chama read_user_cli_args(), executando efetivamente a lógica de código de análise da CLI que você escreveu mais adiante.
"""

"""
Teste no terminal a aplicação, irá aparecer a seguinte mensagem de erro:

usage: weather.py [-h]
weather.py: error: unrecognized arguments: vienna

O Python primeiro imprime informações de uso em seu console. Essas informações sugerem a ajuda interna (-h) fornecida pelo ArgumentParser. 
Em seguida, ele informa que seu analisador não reconheceu o argumento que você passou para o programa usando sua CLI.
"""

"""
° As linhas 15 a 17 definem o argumento "city" que receberá uma ou várias entradas separadas por espaços em branco. 
Ao definir o número de argumentos (nargs) como "+", você permite que os usuários passem nomes de cidades compostos 
por mais de uma palavra, como Nova York.

° As linhas 18 a 23 definem o argumento booleano opcional imperial. Você define o argumento da palavra-chave de ação como 
"store_true", o que significa que o valor para imperial será True se os usuários adicionarem o sinalizador opcional e False se não o fizerem.
"""

"""
No entanto, se você executar o script e passar um nome de cidade como entrada, ainda não poderá ver nenhuma saída exibida de volta ao seu console. 
Volte para weather.py e edite o código em seu bloco de código condicional na parte inferior do arquivo:
"""

if __name__ == "__main__":
    user_args = read_user_cli_args()
    print(user_args.city, user_args.imperial)
