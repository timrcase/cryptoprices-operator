#!/usr/bin/env python3

import kopf
import kubernetes.config as k8s_config
import kubernetes.client as k8s_client
import requests

def get_price(coin, currency):
    coingecko_url = 'https://api.coingecko.com/api/v3/simple/price'
    return requests.get(f'{coingecko_url}?ids={coin}&vs_currencies={currency}').json()[coin][currency]

def create_crypto_price_config_map(namespace, data):
    api_instance = k8s_client.CoreV1Api()
    return api_instance.create_namespaced_config_map(namespace, data)


def update_exchange_rate_config_map(namespace, name, new_data):
    api_instance = k8s_client.CoreV1Api()
    return api_instance.patch_namespaced_config_map(name, namespace, new_data)

@kopf.on.create('operators.timrcase.github.io', 'v1', 'exchangerates')
def on_create(namespace, spec, body, **kwargs):
    coin = ['coin']
    currency = spec['currency']
    price = get_price(coin, currency)
    data = __price_to_config_map_data(price, currency)

    kopf.adopt(data)

    configmap = create_crypto_price_config_map(namespace, data)
    return {'configmap-name': configmap.metadata.name}


@kopf.on.update('operators.timrcase.github.io', 'v1', 'exchangerates')
def on_update(namespace, name, spec, status, **kwargs):
    coin = ['coin']
    currency = spec['currency']
    price = get_price(coin, currency)
    name = status['on_create']['configmap-name']
    data = __price_to_config_map_data(price, currency)

    update_exchange_rate_config_map(namespace, name, data)

def __price_to_config_map_data(price, currency):
    return {
        'data': {
            f'price_{currency}': str(price)
        }
    }