#!/usr/bin/env python3

import kopf
import requests
import json
import os

def get_price(coin, currency):
    coingecko_url = 'https://api.coingecko.com/api/v3/simple/price'
    price = requests.get(f'{coingecko_url}?ids={coin}&vs_currencies={currency}').json()[coin][currency]
    return price

def send_to_slack(coin, currency):
    price = get_price(coin, currency)
    payload = {'text': f'{coin} is currently {price} {str(currency).upper()}'}
    headers = {'Content-Type': 'application/json'}
    slack_wehbook = os.environ.get('SLACK_WEBHOOK_URL')
    requests.post(slack_wehbook, headers=headers, data=json.dumps(payload))

@kopf.on.create('operators.timrcase.github.io', 'v1', 'cryptoprices')
def on_create(spec, **kwargs):
    coin = spec['coin']
    currency = spec['currency']
    send_to_slack(coin, currency)

@kopf.on.update('operators.timrcase.github.io', 'v1', 'cryptoprices')
def on_update(spec, **kwargs):
    coin = spec['coin']
    currency = spec['currency']
    send_to_slack(coin, currency)

@kopf.timer('operators.timrcase.github.io', 'v1', 'exchangerates', interval=3600.0)
def update_price(spec, **kwargs):
    coin = spec['coin']
    currency = spec['currency']
    send_to_slack(coin, currency)