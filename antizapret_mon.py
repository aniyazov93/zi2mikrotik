#!/usr/bin/env python3

import requests
import csv
import ipaddress


def get_antizapret_current_state():
    r = requests.get('http://api.antizapret.info/all.php?type=json')

    if r.status_code != 200:
        return {}

    with open('/tmp/xd123', 'w') as f:
        f.write(r.text)


def read_zi():
    with open('z-i/dump.csv', 'r', encoding="windows-1251") as f:
        reader = csv.reader(f, delimiter=';')

        return list(reader)[1:]


def is_valid_ip(addr):
    try:
        # check what this is valid ipv4
        ip = ipaddress.ip_address(addr)

        # check what this is global address
        return ip.is_global
    except ValueError:
        return False


def is_valid_net(addr):
    try:
        net = ipaddress.ip_network(addr)
        return net.is_global
    except ValueError:
        return False


def separate(data: list):
    banaddrs = [x[0] for x in data]

    values = []

    for banaddr in banaddrs:
        if '|' in banaddr:
            v = [x.strip() for x in banaddr.split('|')]
            values += v
        else:
            values.append(banaddr)

    addresses = []
    networks = []

    for v in values:
        if is_valid_ip(v):
            addresses.append(v)
            continue

        elif is_valid_net(v):
            networks.append(v)
            continue

        else:
            print(v, 'ignored')

    return addresses, networks


if __name__ == '__main__':
    zi_data = read_zi()

    addresses, networks = separate(zi_data)

    print(len(addresses), len(networks))