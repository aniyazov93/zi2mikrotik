import csv
import ipaddress
import requests
import logging

from config import *


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
    banaddrs = list(set([x[0] for x in data]))

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
            logging.warn(f'{str(v)} ignored')

    # post-processing addresses, cleaning from networks-overlapped entries
    # O(n*a). too long
    for n in networks:
        for a in addresses:
            addr_foct = a.split('.')[0]
            net_foct = n.split('.')[0]

            # first octets does not match, no further checks required
            if addr_foct != net_foct:
                continue

            addr = ipaddress.ip_address(a)
            net = ipaddress.ip_network(n)
            if addr in net:
                # print(a, n)
                addresses.remove(a)

    total_banned = len(addresses)

    for n in networks:
        nn = ipaddress.ip_network(n)
        total_banned += nn.num_addresses - 2  # except net and bcast addresses

    return total_banned, addresses, networks


def mikrotik_format(values, gw):
    header = '/ip route'
    str = 'add dst-address={addr} gateway={gw} comment=RKNbanned'

    fvalues = [str.format(addr=v, gw=gw) for v in values]

    return header + '\n' + '\n'.join(fvalues)


def send_tg_message(msg):
    URL = 'https://api.telegram.org/bot'
    TOKEN = TG_BOT_TOKEN

    message_data = {
        'chat_id': TG_CHAT_ID,
        'text': msg,
        'parse_mode': 'HTML'
    }

    try:
        r = requests.post(URL + TOKEN + '/sendMessage', data=message_data)
    except Exception as e:
        print(e)


def check_myservices(networks: list):
    # checking what my ip addresses not in range
    ips = [ipaddress.ip_address(x) for x in ALERT_ADDRESSES]

    nets = [ipaddress.ip_network(x) for x in networks]

    blocked_ips = []

    for i in ips:
        for n in nets:
            if i in n:
                print(f"!!! {str(i)} in blocked network {str(n)} !!!")
                blocked_ips.append((i, n))

    if blocked_ips:
        send_tg_message('<br>'.join([f"!!! {x[0] in x[1]} !!!" for x in blocked_ips]))
