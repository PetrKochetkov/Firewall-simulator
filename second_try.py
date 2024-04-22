import json
import re
import sys
import cv2

mac_regex = r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})'  # Регулярное выражение как маска МАС-адреса
ip_regex = r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'  # IP


def get_config():
    with open("configuration_for_db.json", "r") as file:
        data = json.load(file)
        return data


def valid_mac(mac_address):
    return bool(re.match(mac_regex, mac_address))


def valid_ip(ip_address):
    return bool(re.match(ip_regex, ip_address))


def valid_address(add):
    if valid_ip(add) or valid_mac(add):
        return True
    else:
        return False


class Packet(object):  # Класс пакета, который будет приходить на порт межсетевого экрана
    Source = str()  # Будет иметь вид XXX.XXX.XXX.XXX или XX:XX:XX:XX:XX:XX или XX-XX-XX-XX-XX-XX
    Destination = str()  # Будет иметь вид XXX.XXX.XXX.XXX или XX:XX:XX:XX:XX:XX или XX-XX-XX-XX-XX-XX

    def __init__(self, source_address, destination_address):
        self.Source = str(source_address)
        self.Destination = str(destination_address)

    def __str__(self):
        return "\nАдрес источника: {}\nАдрес назначения: {}\n".format(self.Source, self.Destination)

    def get_src(self):
        return self.Source

    def get_dst(self):
        return self.Destination


def create_packet():
    print('Приступаем к созданию пакета')
    src = input('Введите адрес источника: ')
    dst = input('Введите адрес получателя: ')
    if valid_address(src) and valid_address(dst):
        test_packet = Packet(src, dst)
        return test_packet
    elif not (valid_address(src)):
        print('Неверный адрес источника, вы ввели: {}'.format(src))
        print('Введите данные пакета заново\n')
        create_packet()
    elif not (valid_address(dst)):
        print('Неверный адрес источника, вы ввели: {}'.format(dst))
        print('Введите данные пакета заново\n')
        create_packet()


class Firewall(object):
    mode = None  # Режим работы фаервола, он работает либо с белыми листами, либо с черными
    input = None  # Тут будут находится полученный пакет в виде объекта класса Пакет
    sources = []  # Список адресов источников
    destinations = []  # Список адресов назначений

    def __init__(self, mode, src, dst):
        self.mode = mode
        self.sources = src
        self.destinations = dst

    def check_mode(self):
        if self.mode == "wl":
            pass
        elif self.mode == "bl":
            pass
        elif self.mode == "off":
            print('Межсетевой экран выключен, измените файл конфигурации')
            sys.exit()
        else:
            print("Неверно настроен режим межсетевого экранирования")
            sys.exit()

    def receive(self, input_packet: Packet):
        self.input = input_packet

    def check_of_source_address(self):  # Проверка есть ли адрес источника пакета в списке фаервола
        result = True
        checking_src = self.input.get_src()
        if checking_src in self.sources:
            pass
        else:
            result = False
            print("Проверка адреса источника: {}".format(result))
        return result

    def check_of_destination_address(self):  # Проверка есть ли адрес назначения пакета в списке фаервола
        result = True
        checking_dst = self.input.get_dst()
        if checking_dst in self.destinations:
            pass
        else:
            result = False
            print("Проверка адреса назначения: {}".format(result))
        return result

    def overall_check(self):
        result = True
        print("Режим работы: {}".format(self.mode))
        if self.mode == "wl":  # При работе в режиме белого листа разрешено пропускать то, что есть в списках,
            # остальное нельзя пропускать
            if self.check_of_source_address() and self.check_of_destination_address():
                result = True
            else:
                result = False
        elif self.mode == "bl":  # При работе в режиме черного листа, запрещено тем, кто есть в списках, остальным
            # разрешено
            if self.check_of_destination_address() or self.check_of_source_address():
                result = False
            else:
                result = True
        return result

    def message(self):
        result = self.overall_check()
        if result:
            resulting_message = "Пакет прошел!"
        else:
            resulting_message = "Пакет не прошел!"
        self.input = None
        return resulting_message


conf = get_config()
firewall_mode = conf['mode']
list_of_src = conf['src_list']
list_of_dst = conf['dst_list']
firewall = Firewall(firewall_mode, list_of_src, list_of_dst)  # Создаем фаерволл с заданными параметрами из файла
while True:
    packet = create_packet()  # Создаем пакет
    firewall.receive(packet)  # МЭ получает пакет
    print(firewall.message())  # МЭ проводит проверку и выводит ответ
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
