from flask import Flask
from flask import render_template
from flask import request
from main_part import *
import logging  # для создания логов

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])  # Страница ввода пакета
def put_packet():
    return render_template('input_page.html')


@app.route('/check_packet', methods=['GET', 'POST'])  # Страница вывода ответа
def check_packet():
    source_address = request.form['source_address']
    destination_address = request.form['destination_address']
    try:
        users_packet = create_packet(source_address, destination_address)
        if firewall.check_packet_all(users_packet):
            message = 'Пакет прошел'
        else:
            message = 'Пакет не прошел'
    except InvalidPacketException:
        message = 'Неверно введены данные пакета'
    return render_template('output_page.html', message=message)


@app.route('/settings')  # Страница ввода настроек
def firewall_settings():
    mode = firewall.mode
    match mode:
        case 'wl':
            result_mode = 'White List'
        case 'bl':
            result_mode = 'Black List'
        case 'off':
            result_mode = 'Off'
        case _:
            result_mode = '((('
    src_adds = sorted(firewall.sources)
    dst_adds = sorted(firewall.destinations)
    return render_template('settings.html', mode=result_mode, src_adds=src_adds, dst_adds=dst_adds)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    conf = get_config()
    firewall_mode = conf['mode']
    list_of_src = conf['src_list']
    list_of_dst = conf['dst_list']
    firewall = Firewall(firewall_mode, list_of_src, list_of_dst)  # Создаем фаерволл с заданными параметрами из файла
    app.run(debug=True)

