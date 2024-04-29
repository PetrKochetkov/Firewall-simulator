import json  # для работы с json-файлами


def get_config():
    """Функция для считывания конфигурационных данных из файла
    :return: data -> словарь конфигураций МЭ
    """
    with open("configuration_for_db.json", "r") as file:
        data = json.load(file)
        return data


conf = get_config()
list_of_src = conf['src_list']
print(list_of_src)
