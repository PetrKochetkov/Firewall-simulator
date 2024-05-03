from flask import Flask
from flask import render_template
from main_part import *
import json  # для работы с json-файлами
import re  # для работы с регулярными выражениями
import sys  # для прерывания выполнения программы
import os  # для прерывания выполнения программы
import signal  # для прерывания выполнения программы
import keyboard  # для прерывания выполнения программы
import multiprocessing  # для прерывания выполнения программы
import logging  # для создания логов

app = Flask(__name__)


@app.route('/')  # Страница ввода пакета
def put_packet():
    return render_template('inputting.html')


@app.route('/', methods=['POST'])  # Страница вывода ответа
def receive_packet():
    return 'Lox'


@app.route('/settings')  # Страница ввода настроек
def firewall_settings():
    return render_template('settings.html')


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
    #                     format="%(asctime)s %(levelname)s %(message)s")
    # conf = get_config()
    # firewall_mode = conf['mode']
    # list_of_src = conf['src_list']
    # list_of_dst = conf['dst_list']
    # firewall = Firewall(firewall_mode, list_of_src, list_of_dst)  # Создаем фаерволл с заданными параметрами из файла
    # pid = os.getpid()
    # multiprocessing.Process(target=hook, args=[pid]).start()
    app.run(debug=True)
    # i = 1
    # while True:
    #     while True:
    #         try:
    #             packet = create_packet()  # Создаем пакет
    #             logging.info(f'Создан пакет с данными №{i}')
    #             logging.info(f'Адрес источника {packet.get_src()}')
    #             logging.info(f'Адрес назначения {packet.get_dst()}')
    #             print('\n')
    #             break
    #         except InvalidPacketException:
    #             logging.warning(f'Получена ошибка {InvalidPacketException}')
    #             pass
    #         finally:
    #             i += 1
    #     print(firewall.check_packet(packet))  # МЭ проводит проверку и выводит ответ
    #     print('Конец\n')
