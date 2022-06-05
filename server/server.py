from importlib import import_module
from inspect import getmembers, getdoc, getsourcelines, isfunction
from json.decoder import JSONDecodeError
from pathlib import Path

from flask import Flask, render_template, request, json


app = Flask('test-web-server')

DIR_AUTO_IMPORT = 'auto_import'  # Каталог для размещения модулей доступных для автоимпорта


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
    functions = get_all_functions(DIR_AUTO_IMPORT, '*.py')
    return render_template("all_functions.html", functions=functions, headers=headers)


@app.route('/json/', methods=['POST'])
def response_json():
    module_name, func_name = '', ''
    try:
        request_data = json.loads(request.data)
        module_name = request_data.get('module', '')
        func_name = request_data.get('function', '')
        data = request_data.get('data', '')
        func = getattr(import_module(f'{DIR_AUTO_IMPORT}.{module_name}'), func_name)
        request_data.update({'data': func(data)})
        response = request_data
    except JSONDecodeError:
        response = (f'Полученные данные не JSON', 400)
    except ModuleNotFoundError:
        response = (f'Unknown module "{module_name}"', 500)
    except AttributeError:
        response = (f'Unknown function "{func_name}"', 500)
    return response


if __name__ == "__main__":
    app.run(port=7000)
