import requests
import csv
import ipaddress

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
            print(v, 'ignored')

    # post processing addresses, cleaning from networks-overlapped

    for a in addresses:
        for n in networks:
            if a in n:
                print(a, n)
                addresses.remove(a)

    total_banned = len(addresses)

    for n in networks:
        nn = ipaddress.ip_network(n)
        total_banned += nn.num_addresses - 2  # except net and bcast addresses

    return total_banned, addresses, networks


def mikrotik_format(values, gw):
    header = '/ip routes'
    str = 'add dst-address={addr} gateway={gw} comment=RTKbanned'

    fvalues = [str.format(addr=v, gw=gw) for v in values]

    return header + '\n' + '\n'.join(fvalues)

