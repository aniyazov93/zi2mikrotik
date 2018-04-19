#!/usr/bin/env python3.6

import threading
import atexit
import git
import logging

from time import sleep
from flask import Flask, jsonify, request, Response, redirect

from functions import *

addresses = []
networks = []
total_banned = 0

_lock = threading.Lock()
_th = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def update():
    global addresses, networks, total_banned

    # pulling new zapretinfo data
    logging.info('Pulling new data...')

    g = git.cmd.Git('z-i')
    g.pull()

    logging.info('Parsing...')

    zi_data = read_zi()
    total_banned, addresses, networks = separate(zi_data)

    logging.info(f'Finished. Total IPs: {total_banned}')
    check_myservices(networks)


class Updater(threading.Thread):
    def run(self):
        global _lock
        while True:
            with _lock:
                update()
            sleep(600)


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

    @app.route('/')
    def main_page():
        return redirect('https://github.com/radium88/zi2mikrotik', 307)


    @app.route('/banned_count')
    def count():
        # if _lock.locked():
        #     return '', 204

        print_raw = request.args.get('raw', False, bool)

        if print_raw:
            return str(total_banned)
        else:
            return jsonify({
                'total_banned': total_banned
            })

    @app.route('/info')
    def info():
        # if _lock.locked():
        #     return '', 204

        print_networks = request.args.get('networks', False, bool)
        print_addresses = request.args.get('addresses', False, bool)

        result = {}

        if not (print_networks or print_addresses):
            result = {
                'networks': networks,
                'addresses': addresses
            }
        else:
            if print_addresses:
                result['addresses'] = addresses

            if print_networks:
                result['networks'] = networks

        return jsonify(result)

    @app.route('/mikrotik')
    def mikrotik():
        global networks, addresses
        # if _lock.locked():
        #     return '', 204

        print_networks = request.args.get('networks', False, bool)
        print_addresses = request.args.get('addresses', False, bool)

        gw = request.args.get('gateway')

        if not ((print_networks or print_addresses) and gw):
            return '', 400

        values = []

        if print_addresses:
            values += addresses

        if print_networks:
            values += networks

        response = Response(mikrotik_format(values, gw))
        response.headers['content-type'] = 'text/plain;charset=UTF-8'

        return response

    app.run(host='0.0.0.0', port=3000, threaded=True)

