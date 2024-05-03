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
    users_packet = create_packet(source_address, destination_address)
    if firewall.check_packet_all(users_packet):
        message = 'Пакет прошел'
    else:
        message = 'Пакет не прошел'
    return render_template('output_page.html', message=message)


@app.route('/settings')  # Страница ввода настроек
def firewall_settings():
    return render_template('settings.html')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    conf = get_config()
    firewall_mode = conf['mode']
    list_of_src = conf['src_list']
    list_of_dst = conf['dst_list']
    firewall = Firewall(firewall_mode, list_of_src, list_of_dst)  # Создаем фаерволл с заданными параметрами из файла
    app.run(debug=True)

