import json  # для работы с json-файлами
import re  # для работы с регулярными выражениями
import sys  # для прерывания выполнения программы
import os  # для прерывания выполнения программы
import signal  # для прерывания выполнения программы
import keyboard  # для прерывания выполнения программы
import multiprocessing  # для прерывания выполнения программы


def hook(process_id):
    """Функция "слушает" нажатие клавиш ctrl+1 для прекращения работы программы"""
    while True:
        if keyboard.is_pressed('ctrl + 1'):
            os.kill(process_id, signal.SIGTERM)
            sys.exit(1)


mac_regex = r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})'  # Регулярное выражение как маска МАС-адреса
ip_regex = r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'  # IP


def get_config():
    """Функция для считывания конфигурационных данных из файла
    :return: data -> словарь конфигураций МЭ
    """
    with open("configuration_for_db.json", "r") as file:
        data = json.load(file)
        return data


def valid_mac(mac_address: str) -> bool:
    """Функция для проверки MAC-адреса на корректность формата ввода
    :return: Булево значение, в зависимости от корректности формата ввода
    """
    return bool(re.match(mac_regex, mac_address))


def valid_ip(ip_address: str) -> bool:
    """Функция для проверки IP-адреса на корректность формата ввода
    :return: Булево значение, в зависимости от корректности формата ввода
    """

    return bool(re.match(ip_regex, ip_address))


def valid_address(add: str) -> bool:
    """Проверяет адрес на корректность, в независимости от MAC это или IP адрес
    :return: Булево значение, в зависимости от результата проверки
    """
    if valid_ip(add) or valid_mac(add):
        return True
    else:
        return False


class InvalidPacketException(Exception):
    """Поднимается при неправильном создании пакета"""


class Packet(object):  # Класс пакета, который будет приходить на порт межсетевого экрана
    Source = str()  # Будет иметь вид XXX.XXX.XXX.XXX или XX:XX:XX:XX:XX:XX или XX-XX-XX-XX-XX-XX
    Destination = str()  # Будет иметь вид XXX.XXX.XXX.XXX или XX:XX:XX:XX:XX:XX или XX-XX-XX-XX-XX-XX

    def __init__(self, source_address: str, destination_address: str):
        self.Source = str(source_address)
        self.Destination = str(destination_address)

    def get_src(self):
        """Возвращает адрес источника
        :return: адрес источника в текстовом формате
        """
        return self.Source

    def get_dst(self):
        """Возвращает адрес назначения
        :return: адрес получателя в текстовом формате
        """
        return self.Destination


def create_packet() -> Packet:
    """Создание пакета руками пользователя
    :return: возвращается объект класса Пакет с заданными пользователем адресами, в случае удачных проверок.
    :raise: InvalidPacketException в случае некорректного ввода
    """
    print('Приступаем к созданию пакета')
    src = input('Введите адрес источника: ')
    dst = input('Введите адрес получателя: ')
    test_packet = None
    if valid_address(src) and valid_address(dst):
        test_packet = Packet(src, dst)
    elif not (valid_address(src)):
        print('Неверный адрес источника, вы ввели: {}'.format(src))
        print('Введите данные пакета заново\n')
        raise InvalidPacketException
    elif not (valid_address(dst)):
        print('Неверный адрес получателя, вы ввели: {}'.format(dst))
        print('Введите данные пакета заново\n')
        raise InvalidPacketException
    return test_packet


class Firewall(object):
    mode = None  # Режим работы фаервола, он работает либо с белыми листами, либо с черными листами
    sources = []  # Список адресов источников
    destinations = []  # Список адресов назначений

    def _check_mode(self) -> None:
        """Проверяет режим работы МЭ"""
        match self.mode:
            case "wl":
                pass
            case "bl":
                pass
            case "off":
                print('Межсетевой экран выключен, измените файл конфигурации')
                sys.exit(1)
            case _:
                print("Неверно настроен режим межсетевого экранирования")
                sys.exit(1)

    def __init__(self, mode: str, src: list, dst: list):
        """Создает объект класса Firewall
        :param mode: тип str, получается из JSON, режим МЭ
        :param src: тип list, получается из JSON, содержит список адресов источников
        :param dst: тип list, получается из JSON, содержит список адресов назначений
        """
        self.mode = mode
        self.sources = src
        self.destinations = dst
        self._check_mode()

    def _check_of_source_address(
            self,
            input_packet: Packet
    ) -> bool:  # Проверка есть ли адрес источника пакета в списке фаервола
        """Проверка адреса источника
        :param input_packet: объект класса Packet, создается пользователем
        """
        result = True
        checking_src = input_packet.get_src()
        if checking_src in self.sources:
            pass
        else:
            result = False
        return result

    def _check_of_destination_address(
            self,
            input_packet: Packet
    ) -> bool:  # Проверка есть ли адрес назначения пакета в списке фаервола
        """Проверка адреса назначения
        :param input_packet: объект класса Packet, создается пользователем
        """
        result = True
        checking_dst = input_packet.get_dst()
        if checking_dst in self.destinations:
            pass
        else:
            result = False
        return result

    def _overall_check(self, input_packet: Packet) -> bool:
        """Проверяет пакет на соответствие правилам МЭ
        :param input_packet: объект класса Packet, создается пользователем
        :return: result: Булево значение, в зависимости от проверки
        """
        result = True
        if self.mode == "wl":  # При работе в режиме белого листа разрешено пропускать то, что есть в списках,
            # остальное нельзя пропускать
            if self._check_of_source_address(input_packet) and self._check_of_destination_address(input_packet):
                result = True
            else:
                result = False
        elif self.mode == "bl":  # При работе в режиме черного листа, запрещено тем, кто есть в списках, остальным
            # разрешено
            if self._check_of_destination_address(input_packet) or self._check_of_source_address(input_packet):
                result = False
            else:
                result = True
        return result

    def message(self, input_packet: Packet) -> str:
        """Отправляет результирующее сообщение пользователю
        :param: input_packet: объект класса Packet, создается пользователем
        :return: resulting_message: тип str, возвращает текстовое сообщение
        """
        result = self._overall_check(input_packet)
        if result:
            resulting_message = "Пакет прошел!"
        else:
            resulting_message = "Пакет не прошел!"
        return resulting_message


if __name__ == '__main__':
    conf = get_config()
    firewall_mode = conf['mode']
    list_of_src = conf['src_list']
    list_of_dst = conf['dst_list']
    firewall = Firewall(firewall_mode, list_of_src, list_of_dst)  # Создаем фаерволл с заданными параметрами из файла
    pid = os.getpid()
    multiprocessing.Process(target=hook, args=[pid]).start()
    while True:
        while True:
            try:
                packet = create_packet()  # Создаем пакет
                print('\n')
                break
            except InvalidPacketException:
                pass
        print(firewall.message(packet))  # МЭ проводит проверку и выводит ответ
        print('Конец\n')
# TODO: ввести понятие диапазона адресов
# TODO: ввести веб интерфейс (админ задает правила), (обычный пользователь проверяет свой пакет)
