from flask import Flask
from Process import Process
from threading import Thread
from Consts import Consts
from Scan import Scan
from Enums import State

app = Flask("Process")
process_handler = Process()


@app.route('/addtoqeue/<scanid>/<content>/<timestamp>', methods=['GET', 'POST'])
def add_scan(scanid, content, timestamp):
    newscan = Scan(scanid, content, State.Accepted, timestamp)
    process_handler.add_scan_to_queue(newscan)
    return "Received"


if __name__ == '__main__':
    process_done_thread = Thread(target=process_handler.update_done)
    process_done_thread.start()
    process_scan_thread = Thread(target=process_handler.scan_all)
    process_scan_thread.start()
    app.run(port=Consts.PROCESS_PORT)
