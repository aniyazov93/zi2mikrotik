#!/usr/bin/env python3

import requests


def get_current_state():
    r = requests.get('http://api.antizapret.info/all.php?type=json')

    if r.status_code != 200:
        return {}

    with open('/tmp/xd123', 'w') as f:
        f.write(r.text)


def get_subnets():
    pass


if __name__ == '__main__':
    curstate = get_current_state()
    print(curstate)