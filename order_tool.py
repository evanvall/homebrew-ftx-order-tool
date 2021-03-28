import sys
from typing import List
from ftx import FtxClient
import calculate_orders
from DataClass import Input, Order
from pyfiglet import Figlet



# https://blog.ftx.com/blog/api-authentication/

client = FtxClient(

)
# client._base_url = 'https://ftx.us/api/'


def prepare_orders(orders: List[Order]) -> List[dict]:
    prepared_orders = []
    for order in orders:
        prepared_order = {
            "market": order.market,
            "side": order.side,
            "price": order.price,
            "type": "limit",
            "size": order.size,
            "reduceOnly": True
        }
        prepared_orders.append(prepared_order)
    return prepared_orders


def place_order(order: dict):
    result = client.place_order(
        market=order['market'],
        side=order['side'],
        price=float(order['price']),
        size=float(order['size']))
    print(result)


def place_orders(orders: List[dict]):
    for order in orders:
        place_order(order)


def get_user_input() -> Input:

    market = input('Market: (default: BTC-PERP) ') or 'BTC-PERP'
    market = market.upper()

    while True:
        side = input('Side? (buy/sell): ')
        if side == 'buy' or side == 'sell':
            break

    while True:
        reduce_only = input('Reduce only? (y/N) ')
        if reduce_only == 'y':
            reduce_only = True
            break
        if reduce_only == 'N':
            reduce_only = False
            break

    min_level_price = float(input('Min level price? '))
    min_level_size = float(input('Min level size? '))
    max_level_price = float(input('Max level price? '))
    max_level_size = float(input('Max level size? '))
    distance_between_levels = float(input('Distance between levels? '))
    offset = input('Offset? (default: 0)') or 0.0
    offset = float(offset)

    if min_level_price >= max_level_price:
        raise Exception('Min level price must be less than max level price')

    if side == 'buy' and min_level_size < max_level_size:
        raise Exception('Min level size should be greater than max level size on a buy order')

    if side == 'sell' and min_level_size > max_level_size:
        raise Exception('Min level size should be less than max level size on a sell order')

    return Input(market=market,
                 side=side,
                 reduce_only=reduce_only,
                 min_level_price=min_level_price,
                 min_level_size=min_level_size,
                 max_level_price=max_level_price,
                 max_level_size=max_level_size,
                 distance_between_levels=distance_between_levels,
                 offset=offset)


if __name__ == '__main__':
    print(Figlet(font='rectangles').renderText('FTX Order Manager'))

    user_input: Input = get_user_input()

    print(client.get_orderbook(user_input.market, 1))
    # print(client.get_open_orders(user_input.market))

    orders: List[Order] = calculate_orders.get_orders(
        market=user_input.market,
        side=user_input.side,
        reduce_only=user_input.reduce_only,
        min_level_price=user_input.min_level_price,
        min_level_size=user_input.min_level_size,
        max_level_price=user_input.max_level_price,
        max_level_size=user_input.max_level_size,
        distance_between_levels=user_input.distance_between_levels,
        offset=user_input.offset)

    prepared_orders: List[dict] = prepare_orders(orders)

    while True:
        proceed = input("Place orders? (y/N) ")
        if proceed == 'y':
            break
        if proceed == 'N' or proceed == 'n':
            sys.exit()
        else:
            print('Input not recognized, try again')

    print("Placing orders")
    place_orders(prepared_orders)
