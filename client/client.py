import json
import requests
from json.decoder import JSONDecodeError
import argparse

HOST = 'http://127.0.0.1'
PORT = 7000
URL = '/json/'
FILE = 'json_data.txt'


def get_data_from_server(file_name, host, port, url):
    try:
        with open(file_name, encoding='UTF-8') as file:
            data = json.loads(file.read())
        response = requests.post(f'{host}:{port}{url}', data=json.dumps(data))
        res = response.text
    except JSONDecodeError:
        res = f'Данные в файле "{file_name}" не JSON'
    except FileNotFoundError:
        res = f'Файл с данными "{file_name}" не существует.'
    except OSError as err:
        res = str(err)
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for send POST data to server and get answer')
    parser.add_argument('-file_name', type=str, default=FILE,
                        help=f'File with JSON data for send to the server (default: {FILE})')
    parser.add_argument('-host', type=str, default=HOST, help=f'Host of server (default: {HOST})')
    parser.add_argument('-port', type=int, default=PORT, help=f'Port (default: {PORT})')
    parser.add_argument('-url', type=str, default=URL, help=f'URL (default: {URL})')
    args = parser.parse_args()
    print(get_data_from_server(args.file_name, args.host, args.port, args.url))
