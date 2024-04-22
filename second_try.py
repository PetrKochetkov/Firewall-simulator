import json


def get_config():
    with open("configuration_for_db.json", "r") as file:
        data = json.load(file)
        return data


class Packet(object):  # Класс пакета, который будет приходить на порт межсетевого экрана
    Source = str()  # Будет иметь вид 255.255.255.255 или XX-XX-XX-XX-XX-XX
    Destination = str()  # Будет иметь вид 255.255.255.255 или XX-XX-XX-XX-XX-XX

    def __init__(self, source_address, destination_address, contents, packet_protocols, application_protocols):
        self.Source = source_address
        self.Destination = destination_address


class Firewall(object):
    mode = None  # Режим работы фаервола, он работает либо с белыми листами, либо с черными
    Received_packet = None  # Тут будут находится полученные пакеты

    def __init__(self, mode):
        self.mode = mode

    def check_of_source_address(self, packet):
        pass

    def check_of_destination_address(self, packet):
        pass

    def overall_check(self):
        pass


class DataBase(object):
    approved_sources = []
    approved_destinations = []


conf = get_config()
firewall_mode = conf['mode']
list_of_src = conf['src_list']
list_of_dst = conf['dst_list']
