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
    payload = {'text': f'{coin} is currently {price:,.2f} {str(currency).upper()}'}
    headers = {'Content-Type': 'application/json'}
    slack_wehbook = os.environ.get('SLACK_WEBHOOK_URL')
    requests.post(slack_wehbook, headers=headers, data=json.dumps(payload))

## Timer executes at creation and on the cadence defined by the interval
## Create executes once at creation if that is preferred
# @kopf.on.create('operators.timrcase.github.io', 'v1', 'cryptoprices')
@kopf.timer('operators.timrcase.github.io', 'v1', 'cryptoprices', interval=3600.0)
def update_price(spec, **kwargs):
    coin = spec['coin']
    currency = spec['currency']
    send_to_slack(coin, currency)

## Executes any time the custom resource is changed
@kopf.on.update('operators.timrcase.github.io', 'v1', 'cryptoprices')
def on_update(spec, **kwargs):
    coin = spec['coin']
    currency = spec['currency']
    send_to_slack(coin, currency)
