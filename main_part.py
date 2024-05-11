import json  # for working with json-files
import re  # for working with regular expressions
import logging  # for logging
import sys

mac_regex = r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})'  # regular expressions as mask for MAC address
ip_regex = r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'
# same for IP address


def get_config():
    """For reading configuration data from .json file
    :return: data -> data in dictionary format
    """
    with open("configuration_for_db.json", "r") as file:
        data = json.load(file)
        return data


def valid_mac(mac_address: str) -> bool:
    """For checking MAC address correct input format
    :return: Boolean value, depending on the correctness of the input format
    """
    return bool(re.match(mac_regex, mac_address))


def valid_ip(ip_address: str) -> bool:
    """For checking IP address correct input format
    :return:  Boolean value, depending on the correctness of the input format
    """
    return bool(re.match(ip_regex, ip_address))


def valid_address(add: str) -> bool:
    """Checks the address for correctness, regardless of whether it is a MAC or IP address
    :return: Boolean value, depending on the correctness of the input format
    """
    if valid_ip(add) or valid_mac(add):
        return True
    else:
        return False


def ip_to_dec(x: str) -> bin:
    """ Converts an IP address to a decimal number
    :param x: string IP address
    :return: result_address: IP converted to decimal
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
    """Raises when the package is created incorrectly"""


class InvalidSettingsError(Exception):
    """Raises when the firewall settings are incorrect"""


class Packet(object):  # Class of the packet that will arrive at the firewall
    Source = str()  # Looks like XXX.XXX.XXX.XXX or XX:XX:XX:XX:XX:XX
    Destination = str()  # Looks like XXX.XXX.XXX.XXX or XX:XX:XX:XX:XX:XX

    def __init__(self, source_address: str, destination_address: str):
        self.Source = str(source_address)
        self.Destination = str(destination_address)

    def get_src(self):
        """Gets source address from Packet object
        :return: source address in text format
        """
        return self.Source

    def get_dst(self):
        """Gets destination address from Packet object
        :return: destination address in text format
        """
        return self.Destination


def create_packet(src: str, dst: str) -> Packet:
    """Creating a package by user's hand
    :param src: Source address
    :param dst: Destination address
    :return: an object of the Package class with user-specified addresses, in case of successful checks
    :raise InvalidPacketException in case of incorrect input
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
    mode = None  # Firewall operating mode, it works with either white lists (wl) or black lists (bl)
    sources = []  # List of source addresses
    destinations = []  # List of destination addresses

    @staticmethod
    def _check_mode(new_mode: str) -> None:
        """Checks the operating mode of the FW"""
        match new_mode:
            case "wl":
                pass
            case "bl":
                pass
            case "off":
                pass
            case _:
                raise InvalidSettingsError('Incorrect working mode')

    @staticmethod
    def _check_address(list_of_addresses):
        for element in list_of_addresses:
            if valid_address(element):
                pass
            else:
                raise InvalidSettingsError('Invalid address format')

    def __init__(self, mode: str, src: list, dst: list):
        """Creates an object of the Firewall class
        :param mode: str type, obtained from JSON, Firewall mode
        :param src: list type, obtained from JSON, contains a list of source addresses
        :param dst: list type, obtained from JSON, contains a list of destination addresses
        """

        try:
            self._check_mode(mode)
            # self._check_address(src) # Все ломается из за диапазонов
            # self._check_address(dst) # Все ломается из за диапазонов
            self.mode = mode
            self.sources = src
            self.destinations = dst
        except InvalidSettingsError:
            sys.exit(1)

    def _check_of_source_address(self, input_packet: Packet) -> bool:
        """Checking whether the packet source address is in the firewall list
        :param input_packet: an object of the Packet class, created by the user
        """
        logging.info('Checking the source address')
        logging.info(f'Allowed source addresses: {self.sources}')
        checking_src = input_packet.get_src()
        input_add_dec = ip_to_dec(checking_src)
        result = True
        for element in self.sources:
            if element.find('-') == -1:  # Checks that the addresses element is just an address and not a range
                if checking_src == element:
                    logging.info(f'The address being checked {checking_src} is in the list')
                    result = True
                    break
                else:
                    logging.info(
                        f'The address being checked is not in the list, compare the entered {checking_src} and'
                        f' the given {element}')
                    result = False
            elif element.find('-') != -1:  # Check that the address element is a range of addresses
                address_range = element.split('-')
                range_start = address_range[0]
                range_start_dec = ip_to_dec(range_start)
                range_end = address_range[1]
                range_end_dec = ip_to_dec(range_end)
                if (input_add_dec >= range_start_dec) and (input_add_dec <= range_end_dec):
                    logging.info(
                        f'The address being checked {checking_src} is in the address range from {range_start}'
                        f' to {range_end}')
                    result = True
                    break
                else:
                    logging.info(
                        f'The address being checked {checking_src} is not in the address range from {range_start}'
                        f' to {range_end}')
                    result = False
        logging.info(f'The result of checking the source address {result} in the list of addresses')
        return result

    def _check_of_destination_address(self, input_packet: Packet) -> bool:
        """Проверка есть ли адрес назначения пакета в списке фаервола
        :param input_packet: an object of the Packet class, created by the user
        """
        logging.info('Checking the destination address')
        logging.info(f'Allowed destinations: {self.destinations}')
        checking_dst = input_packet.get_dst()
        input_add_dec = ip_to_dec(checking_dst)
        result = True
        for element in self.destinations:
            if element.find('-') == -1:  # Check that the addresses element is just an address and
                # not a range of addresses
                if checking_dst == element:
                    logging.info(f'The address being checked {checking_dst} is in the list')
                    result = True
                    break
                else:
                    logging.info(
                        f'The address being checked is not in the list, compare the entered {checking_dst} and the'
                        f' given {element}')
                    result = False
            elif element.find('-') != -1:  # Check that the address element is a range of addresses
                address_range = element.split('-')
                range_start = address_range[0]
                range_start_dec = ip_to_dec(range_start)
                range_end = address_range[1]
                range_end_dec = ip_to_dec(range_end)
                if (input_add_dec >= range_start_dec) and (input_add_dec <= range_end_dec):
                    logging.info(
                        f'The address being checked {checking_dst} is in the address range from {range_start}'
                        f' to {range_end}')
                    result = True
                    break
                else:
                    logging.info(
                        f'The address being checked {checking_dst} is not in the range'
                        f' addresses from {range_start} to {range_end}')
                    result = False
        logging.info(f'Destination address check result {result}')
        return result

    def _overall_check(self, input_packet: Packet) -> bool:
        """Checks the package for compliance with firewall rules
        :param input_packet: an object of the Packet class, created by the user
        :return: result: Boolean value, depending on the check
        """
        result = True
        if self.mode == "wl":  # When working in white list mode, it is allowed to skip what is in the lists,
            # you can't skip the rest
            if self._check_of_source_address(input_packet) and self._check_of_destination_address(input_packet):
                result = True
            else:
                result = False
        elif self.mode == "bl":  # When working in blacklist mode, it is prohibited for those who are on the lists,
            # the rest allowed
            if self._check_of_destination_address(input_packet) or self._check_of_source_address(input_packet):
                result = False
            else:
                result = True
        elif self.mode == "off":
            result = True
        logging.info(f'The result of the entire check {result}')
        return result

    def change_settings(self, new_mode: str, new_sources: list, new_destinations: list) -> None:
        """Changes settings of firewall if input data is in normal form, otherwise raises Error and stop program"""
        try:
            self._check_mode(new_mode)
            # self._check_address(new_sources) #Все ломается из за диапазонов
            # self._check_address(new_destinations) #Все ломается из за диапазонов
            self.mode = new_mode
            self.sources = new_sources
            self.destinations = new_destinations
        except InvalidSettingsError:
            sys.exit(1)

    def check_packet_all(self, input_packet: Packet) -> bool:
        """Sends the resulting message to the user
        :param input_packet: an object of the Packet class, created by the user
        :return: resulting_message: type bool
        """
        result = self._overall_check(input_packet)
        if result:
            resulting_message = True
        else:
            resulting_message = False
        return resulting_message
