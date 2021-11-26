from flask import Flask
from Data import Data
from Scan import Scan
from Enums import State
from Consts import Consts
from datetime import datetime
from json import JSONEncoder
from threading import Thread


app = Flask("Data Layer")
data_handler = Data()


@app.route('/addscan/<scanid>/<content>/<timestamp>', methods=['GET', 'POST'])
def add_new_scan(scanid, content, timestamp):
    newscan = Scan(scanid, content, str(State.Accepted), timestamp)
    data_handler.add_scan(scanid, newscan)
    return "Added new scan: " + str(scanid), + ", " + str(content)


@app.route('/updatescan/<scanid>/<content>/<state>/<timestamp>', methods=['GET', 'POST'])
def update_scan(scanid, content, state, timestamp):
    newscan = Scan(scanid, content, str(state), timestamp)
    data_handler.add_scan(scanid, newscan)
    return "Added new scan: " + str(scanid) + ", " + str(content)


@app.route('/setstatus/<scanid>/<status>', methods=['GET', 'POST'])
def set_scan_status(scanid, status):
    data_handler.set_scan_status(scanid, status)
    return "Changed to " + str(status)


@app.route('/status/<scanid>', methods=['GET', 'POST'])
def get_status(scanid):
    return str(data_handler.get_scan_status(scanid))


@app.route('/status', methods=['GET', 'POST'])
def get_all():
    json = data_handler.get_all_json()
    return json


if __name__ == '__main__':
    clean_thread = Thread(target=data_handler.clean_overdue)
    clean_thread.start()
    app.run(port=Consts.DATA_PORT)
