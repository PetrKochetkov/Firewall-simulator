class Data(object):
    Destination_address = int()  # Destination MAC-address, Destination IP-address, Destination Port
    Source_address = int()  # Source MAC-address, Source IP-address, Source Port
    flag = str()  # Different flags. For each layer different flags
    TTL = int()  # Only for Network layer, else = -1

    def __init__(self, destination_address, source_address, flag, ttl=-1):  # -1, так как только у IP есть TTL
        self.Destination_address = destination_address
        self.Source_address = source_address
        self.flag = flag
        self.TTL = ttl


class Frame(Data):  # Link layer, based on MAC protocol

    def __init__(self, destination_mac, source_mac, flag):
        super().__init__(destination_mac, source_mac, flag)


class Packet(Data):  # Internet layer, based on IP

    def __init__(self, destination_ip, source_ip, flag, ttl):
        super().__init__(destination_ip, source_ip, flag, ttl)


class Segment(Data):  # Transport layer, based on TCP

    def __init__(self, destination_port, source_port, flag):
        super().__init__(destination_port, source_port, flag)
