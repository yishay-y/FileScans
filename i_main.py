from flask import Flask
from Ingest import Ingest
from Consts import Consts


app = Flask("Ingest")
ingest_handler = Ingest()


@app.route('/addscan/<content>', methods=['GET', 'POST'])
def add_new_scan(content):
    return str(ingest_handler.add_scan(content))


if __name__ == '__main__':
    app.run(port=Consts.INGEST_PORT)
