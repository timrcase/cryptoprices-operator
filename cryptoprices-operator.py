#!/usr/bin/env python3

import kopf
import kubernetes.config as k8s_config
import kubernetes.client as k8s_client
import requests

def get_price(coin, currency):
    coingecko_url = 'https://api.coingecko.com/api/v3/simple/price'
    return requests.get(f'{coingecko_url}?ids={coin}&vs_currencies={currency}').json()[coin][currency]

@kopf.on.create('operators.timrcase.github.io', 'v1', 'cryptoprices')
def on_create(namespace, spec, body, **kwargs):
    coin = spec['coin']
    currency = spec['currency']
    print(get_price(coin, currency))

@kopf.on.update('operators.timrcase.github.io', 'v1', 'cryptoprices')
def on_update(namespace, name, spec, status, **kwargs):
    coin = spec['coin']
    currency = spec['currency']
    print(get_price(coin, currency))