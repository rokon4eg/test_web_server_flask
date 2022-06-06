import argparse
import json
from importlib import import_module
from inspect import getmembers, getdoc, getsourcelines, isfunction
from json.decoder import JSONDecodeError
from pathlib import Path

from flask import Flask, render_template, request


app = Flask('test-web-server')

DIR_AUTO_IMPORT = 'auto_import'  # Каталог для размещения модулей доступных для автоимпорта
PORT = 7000


@app.route('/')
def hello():
    return 'This is test-web-server'


def get_all_functions(dir_, file_mask):
    path = Path.cwd() / dir_
    file_list = path.glob(file_mask)
    res = []
    for module in file_list:
        module_funcs = getmembers(import_module(f'{dir_}.{module.stem}'), isfunction)  # Получаем список всех функций модуля
        for name_func, func in module_funcs:
            doc_func = getdoc(func)  # Doc strings
            code_func = getsourcelines(func)[0]  # код функции
            code_func = '<pre><code>' + ''.join(code_func) + '</code></pre>'
            line = [module.stem, name_func, doc_func, code_func]
            res.append(line)
    return res


@app.route('/html/')
def display_all_functions():
    headers = ['Модуль', 'Функция', 'Описание', 'Код']
    functions = get_all_functions(autoimport_module_dir, '*.py')
    return render_template('all_functions.html', functions=functions, headers=headers)


@app.route('/json/', methods=['POST'])
def response_json():
    module_name = func_name = ''
    try:
        request_data = json.loads(request.data)
        module_name = request_data.get('module', '')
        func_name = request_data.get('function', '')
        data = request_data.get('data', '')
        func = getattr(import_module(f'{autoimport_module_dir}.{module_name}'), func_name)
        request_data['data'] = func(data)
        response = json.dumps(request_data)
    except JSONDecodeError:
        response = (f'Полученные данные не JSON', 400)
    except ValueError as err:
        response = (str(err), 400)
    except ModuleNotFoundError:
        response = (f'Unknown module "{module_name}"', 500)
    except AttributeError:
        response = (f'Unknown function "{func_name}"', 500)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server for get POST data from client and send answer')
    parser.add_argument('-port', type=int, default=PORT, help=f'Port (default: {PORT})')
    parser.add_argument('-dir', type=str, default=DIR_AUTO_IMPORT,
                        help=f'Directory on the server with autoimport modules (default: {DIR_AUTO_IMPORT})')
    args = parser.parse_args()
    autoimport_module_dir = args.dir
    app.run(port=args.port, debug=True)
