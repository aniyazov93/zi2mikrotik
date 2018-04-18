#!/usr/bin/env python3

import requests

responce = requests.get('https://2018.schors.spb.ru/d1_ipblock.json')

print(responce.json()[-1])