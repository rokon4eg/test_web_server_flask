def mytest(data: dict):
    """
    Функция сортирует список по правилам сортировки версий (2.11 больше 2.9, 2.1.11 больше 2.1.9 и т.д.).
    Поле "value" меняет строковое значение на массив из слов, удаляя все символы “ “ вокруг.
    После этого обработанные данные возвращаются клиенту
    """
    items = list(data.items())
    try:
        items.sort(key=lambda item: [int(num) for num in item[1].get('ident', '').split('.')])
        for item in items:
            item[1].update({'value': item[1].get('value', '').split()})
        sorted_data = dict(items)
        return sorted_data
    except ValueError:
        raise
