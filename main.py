""" Ethereum Transaction Tracker. """

import requests
from datetime import datetime
import matplotlib.pyplot as plt
import config


""" Variables """

ETHERSCAN_API_KEY = config.ETHERSCAN_API_KEY
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'

""" Functions """


def get_eth_balance(wallet_address):
    """ Returns the ETH balance of the given address. """
    params = {
        'module': 'account',
        'action': 'balance',
        'address': wallet_address,
        'tag': 'latest',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()
    balance_wei = int(data['result'])
    balance_eth = balance_wei / 1e18
    return balance_eth


def get_transactions(wallet_address):
    """ Returns a list of transactions for the given address. """
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet_address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()
    transactions = data['result']
    return transactions


def plot_transactions(wallet_address):
    """ Plots the transactions for the given address. """
    transactions = get_transactions(wallet_address)
    timestamps = [datetime.utcfromtimestamp(int(tx['timeStamp'])).strftime('%H:%M:%S\n%d-%m-%y') for tx in transactions]
    values = [int(tx['value']) / 1e18 for tx in transactions]

    plt.plot(timestamps, values, marker='o')
    plt.gcf().autofmt_xdate()  # Rotate date labels
    plt.title(f'Ethereum Transactions Address:\n{wallet_address}')
    plt.xlabel(f'--> {str(get_eth_balance(wallet_address))[:4]} ETH <--')
    plt.ylabel('Value in ETH')
    plt.show()


""" Main program """

if __name__ == '__main__':
    address = input("Enter Ethereum address: ")
    print(f"Balance: {get_eth_balance(address)} ETH")
    plot_transactions(address)
