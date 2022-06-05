def mytest(data: dict):
    """
    Функция сортирует список по правилам сортировки версий (2.11 больше 2.9, 2.1.11 больше 2.1.9 и т.д.).
    Поле "value" меняет строковое значение на массив из слов, удаляя все символы “ “ вокруг.
    После этого обработанные данные возвращаются клиенту
    """
    values = list(data.values())
    values.sort(key=lambda value: [int(num) for num in value.get('ident').split('.')])
    [item.update({'value': item.get('value').split()}) for item in values]
    sorted_data = dict(zip(data.keys(), values))
    return sorted_data