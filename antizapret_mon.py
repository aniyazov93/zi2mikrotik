#!/usr/bin/env python3

import ipaddress
import threading
import atexit

from time import sleep
from flask import Flask, jsonify, make_response

from functions import *

addresses = []
networks = []
_lock = threading.Lock()
_th = None


def update():
    global addresses, networks
    print('Updating info...')
    zi_data = read_zi()
    addresses, networks = separate(zi_data)
    print('Finished')


class Updater(threading.Thread):
    def run(self):
        global _lock
        while True:
            with _lock:
                update()
            sleep(120)


def create_app():
    global _th
    app = Flask(__name__)

    def interrupt():
        global _th
        _th.cancel()

    _th = Updater()
    _th.start()

    atexit.register(interrupt)

    return app


if __name__ == '__main__':
    app = create_app()


    @app.route('/info')
    def info():
        if _lock.locked():
            return '', 204

        return jsonify({
            'networks': networks,
            'addresses': addresses
        })

    app.run(host='0.0.0.0', port=3000, threaded=True)