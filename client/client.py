import json
import requests
from json.decoder import JSONDecodeError

HOST = 'http://127.0.0.1'
PORT = 7000
URL = '/json/'
FILE = 'json_data.txt'


def get_sorted_data_from_server(file_name, host, port, url):
    try:
        with open(file_name, encoding='UTF-8') as file:
            data = json.loads(file.read())
        response = requests.post(f'{host}:{port}{url}', data=json.dumps(data))
        res = response.text
    except JSONDecodeError:
        res = f'Данные в файле "{file_name}" не JSON'
    except FileNotFoundError:
        res = f'Файл с данными "{file_name}" не существует.'
    return res


if __name__ == '__main__':
    print(get_sorted_data_from_server(FILE, HOST, PORT, URL))
