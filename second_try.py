from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()
table_of_approved_sources = Table("approved_sources", metadata_obj,
                                  Column("id", Integer, primary_key=True),
                                  Column("source", String(30)))

table_of_approved_destinations = Table("approved_destinations", metadata_obj,
                                       Column("id", Integer, primary_key=True),
                                       Column("destinations", String(30)))

table_of_approved_content = Table("approved_content", metadata_obj,
                                  Column("id", Integer, primary_key=True),
                                  Column("content", String(30)))

table_of_approved_packet_protocols = Table("approved_packet_protocols", metadata_obj,
                                           Column("id", Integer, primary_key=True),
                                           Column("packet_protocols", String(30)))

table_of_approved_app_protocols = Table("approved_app_protocols", metadata_obj,
                                        Column("id", Integer, primary_key=True),
                                        Column("app_protocols", String(30)))

password = 'root'
database_name = 'Approved'


class Packet(object):  # Класс пакета, который будет приходить на порт межсетевого экрана
    Source = str()  # Будет иметь вид 255.255.255.255:65534
    Destination = str()  # Будет иметь вид 255.255.255.255:65534
    Contents = str()  # Контент, который находится в пакете, пока не знаю как проверять
    Packet_protocols = []  # Протоколы, которые используются при передаче пакета
    Application_protocols = []  # Протоколы, которые используются при

    def __init__(self, source_address, destination_address, contents, packet_protocols, application_protocols):
        self.Source = source_address
        self.Destination = destination_address
        self.Contents = contents
        self.Packet_protocols = packet_protocols
        self.Application_protocols = application_protocols


class Firewall(object):
    Received_packet = None  # Тут будут находится полученные пакеты

    def check_of_source_address(self, packet):
        pass

    def check_of_destination_address(self, packet):
        pass

    def check_of_contents(self, packet):
        pass

    def check_of_packet_protocols(self, packet):
        pass

    def check_of_app_protocols(self, packet):
        pass

    def overall_check(self):
        pass


class DataBase(object):
    approved_sources = []
    approved_destinations = []
    approved_content = []
    approved_packet_protocols = []
    approved_app_protocols = []

    def get_values_from_table(self, table_name):
        list_of_data = []
        with engine.connect() as conn:
            result = conn.execute(text(f'SELECT x, y FROM {table_name}'))
            for element in result:
                list_of_data.append(element)  # Берем из таблицы значения
            conn.commit()
