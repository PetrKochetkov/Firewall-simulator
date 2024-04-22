import json
import socket
import re

address = input("Введите адрес: ")

mac_regex = r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})'
ip_regex = r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'


def valid_mac(mac_address):
    return bool(re.match(mac_regex, mac_address))


def valid_ip(ip_address):
    return bool(re.match(ip_regex, ip_address))


def valid_address(add):
    if valid_ip(add) or valid_mac(add):
        return True
    else:
        return False


print(address, "->", valid_address(address))
