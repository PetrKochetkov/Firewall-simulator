from flask import Flask
from flask import render_template
from flask import request
from main_part import *
from json import JSONDecodeError
import logging  # для создания логов

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])  # Страница ввода пакета и вывода результата
def put_packet():
    if request.method == 'GET':
        return render_template('input_page.html')
    if request.method == 'POST':
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


@app.route('/settings', methods=['GET', 'POST'])
def something():
    if request.method == 'GET':
        mode = firewall.mode
        match mode:
            case 'wl':
                result_mode = 'wl'
            case 'bl':
                result_mode = 'bl'
            case 'off':
                result_mode = 'off'
            case _:
                result_mode = '((('
        src_adds = sorted(firewall.sources)
        dst_adds = sorted(firewall.destinations)
        return render_template('settings.html', mode=result_mode, src_adds=src_adds, dst_adds=dst_adds)
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_mode = data['mode']
            new_src_adds = data['src_list']
            new_dst_adds = data['dst_list']
            firewall.change_settings(new_mode=new_mode, new_sources=new_src_adds, new_destinations=new_dst_adds)
            new_settings = json.dumps(data)
            with open('configuration_for_db.json', 'w') as file:
                file.write(new_settings)
            return '', 200
        except (JSONDecodeError, KeyError):
            return '', 400


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    conf = get_config()
    firewall_mode = conf['mode']
    list_of_src = conf['src_list']
    list_of_dst = conf['dst_list']
    firewall = Firewall(firewall_mode, list_of_src, list_of_dst)  # Создаем фаерволл с заданными параметрами из файла
    app.run(debug=True)
