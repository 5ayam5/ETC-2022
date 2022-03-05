#!/usr/bin/python
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function
from re import S

import sys
import socket
import json
import bond

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name = "INTRATERRESTRIALCREATURES"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index = 0
prod_exchange_hostname = "production"

symbols = {}
symbol_counts = {}
order_id = 1

port = 25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile("rw", 1)


def write_to_exchange(exchange, obj):
    print("Message sent: ", obj, file=sys.stderr)
    json.dump(obj, exchange)
    exchange.write("\n")


def read_from_exchange(exchange):
    return json.loads(exchange.readline())


def update_details(exchange):
    message = read_from_exchange(exchange)
    print("The exchange replied:", message, file=sys.stderr)
    if message["type"] == "open":
        for syms in message["symbols"]:
            symbols[syms] = ([], [])
            symbol_counts[syms] = 0
    elif message["type"] == "close":
        for syms in message["symbols"]:
            symbols.pop(syms)
    elif message["type"] == "book":
        symbols[message["symbol"]] = (message["buy"], message["sell"])
    elif message["type"] == "fill":
        symbol_counts[message["symbol"]] += (1 if message["dir"] == "BUY" else -1) * message["size"]
    elif message["type"] == "ack":
        return (True, message["order_id"])
    elif message["type"] == "reject":
        return (False, (message["order_id"], message["error"]))



def get_ack(exchange):
    while True:
        ret = update_details(exchange)
        if ret is not None:
            return ret

def transaction(exchange, symbol, price, quantity, direction):
    global order_id
    print(order_id)
    write_to_exchange(exchange, {"type": "add", "order_id": order_id,
                          "symbol": symbol, "dir": direction, "price": price, "size": quantity})
    order_id += 1
    print(order_id)
    return get_ack(exchange)

# ~~~~~============== MAIN LOOP ==============~~~~~


def main():
    global order_id
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    i = 0
    while i < 10:
        update_details(exchange)
        message = read_from_exchange(exchange)
        print("The exchange replied:", message, file=sys.stderr)
        transaction(exchange, "BOND", 1001, 1, "SELL")
        for order in bond.bond_order(symbols["BOND"][0], symbols["BOND"][1]):
            transaction(exchange, order["symbol"], order["price"], order["size"], order["dir"])


if __name__ == "__main__":
    main()
