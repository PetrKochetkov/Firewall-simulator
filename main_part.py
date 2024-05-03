import json  # для работы с json-файлами
import re  # для работы с регулярными выражениями
import sys  # для прерывания выполнения программы
import os  # для прерывания выполнения программы
import signal  # для прерывания выполнения программы
import keyboard  # для прерывания выполнения программы
import multiprocessing  # для прерывания выполнения программы
import logging  # для создания логов


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


def ip_to_dec(x: str) -> bin:
    """ Переделывает IP адрес в десятичное число
    :param x: str IP адрес
    :return: result_address: IP переделанный в десятичное число
    """
    list_add = x.split('.')  # ['XXX', 'XXX', 'XXX', 'XXX']
    address = []
    for element in list_add:
        part = format(int(element), 'b')
        address.append(part)
    for index in range(len(address)):
        while len(address[index]) <= 7:
            address[index] = '0' + address[index]
    result_address = int(''.join(address), 2)
    return result_address


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


def create_packet(src: str, dst: str) -> Packet:
    """Создание пакета руками пользователя
    :param src: Адрес источника
    :param dst: Адрес назначения
    :return: возвращается объект класса Пакет с заданными пользователем адресами, в случае удачных проверок.
    :raise InvalidPacketException в случае некорректного ввода
    """
    test_packet = None
    if valid_address(src) and valid_address(dst):
        test_packet = Packet(src, dst)
    elif not (valid_address(src)):
        raise InvalidPacketException
    elif not (valid_address(dst)):
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

    def _check_of_source_address(self, input_packet: Packet) -> bool:  # Проверка есть ли адрес источника пакета
        # в списке фаервола
        """Проверка адреса источника
        :param input_packet: объект класса Packet, создается пользователем
        """
        logging.info('Проверяем адрес источника')
        logging.info(f'разрешенные адреса источника: {self.sources}')
        checking_src = input_packet.get_src()
        input_add_dec = ip_to_dec(checking_src)
        result = True
        for element in self.sources:
            if element.find('-') == -1:  # Проверяем что элемент адресов просто адрес
                if checking_src == element:
                    logging.info('Проверяемый адрес есть в списке')
                    result = True
                    break
                else:
                    logging.info(
                        f'Проверяемого адреса нет в списке, сравнили введенный {checking_src} и данный {element}')
                    result = False
            elif element.find('-') != -1:  # Проверяем что элемент адресов диапазон адресов
                address_range = element.split('-')
                range_start = address_range[0]
                range_start_dec = ip_to_dec(range_start)
                range_end = address_range[1]
                range_end_dec = ip_to_dec(range_end)
                if (input_add_dec >= range_start_dec) and (input_add_dec <= range_end_dec):
                    logging.info(
                        f'Проверяемый адрес {checking_src} есть в диапазоне адресов от {range_start} до {range_end}')
                    result = True
                    break
                else:
                    logging.info(
                        f'Проверяемого адреса {checking_src} нет в диапазоне адресов от {range_start} до {range_end}')
                    result = False
        logging.info(f'Результат проверки адреса источника {result}')
        return result

    def _check_of_destination_address(self, input_packet: Packet
                                      ) -> bool:  # Проверка есть ли адрес назначения пакета в списке фаервола
        """Проверка адреса назначения
        :param input_packet: объект класса Packet, создается пользователем
        """
        logging.info('Проверяем адрес назначения')
        logging.info(f'разрешенные адреса назначения: {self.destinations}')
        checking_dst = input_packet.get_dst()
        input_add_dec = ip_to_dec(checking_dst)
        result = True
        for element in self.destinations:
            if element.find('-') == -1:  # Проверяем что элемент адресов просто адрес
                if checking_dst == element:
                    logging.info('Проверяемый адрес есть в списке')
                    result = True
                    break
                else:
                    logging.info(
                        f'Проверяемого адреса нет в списке, сравнили введенный {checking_dst} и данный {element}')
                    result = False
            elif element.find('-') != -1:  # Проверяем что элемент адресов диапазон адресов
                address_range = element.split('-')
                range_start = address_range[0]
                range_start_dec = ip_to_dec(range_start)
                range_end = address_range[1]
                range_end_dec = ip_to_dec(range_end)
                if (input_add_dec >= range_start_dec) and (input_add_dec <= range_end_dec):
                    logging.info(
                        f'Проверяемый адрес {checking_dst} есть в диапазоне адресов от {range_start} до {range_end}')
                    result = True
                    break
                else:
                    logging.info(
                        f'Проверяемый адрес {checking_dst} отсутствует в диапазоне адресов от {range_start} до {range_end}')
                    result = False
        logging.info(f'Результат проверки адреса назначения {result}')
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
        logging.info(f'Результат всей проверки {result}')
        return result

    def check_packet_all(self, input_packet: Packet) -> bool:
        """Отправляет результирующее сообщение пользователю
        :param: input_packet: объект класса Packet, создается пользователем
        :return: resulting_message: тип str, возвращает текстовое сообщение
        """
        result = self._overall_check(input_packet)
        if result:
            resulting_message = True
        else:
            resulting_message = False
        return resulting_message


