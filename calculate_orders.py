import numpy as np
from typing import List
from DataClass import Order


def calculate_slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)


def calculate_y_intercept(x1, y1, slope):
    return slope * (-x1) + y1


def get_y_value(slope, y_intercept, x):
    return slope * x + y_intercept


def get_orders(market: str,
               side: str,
               reduce_only: bool,
               min_level_price: float,
               min_level_size: float,
               max_level_price: float,
               max_level_size: float,
               distance_between_levels: float,
               offset: float) -> List[Order]:

    slope = calculate_slope(min_level_price, min_level_size, max_level_price, max_level_size)
    y_intercept = calculate_y_intercept(min_level_price, min_level_size, slope)

    prices = np.arange(min_level_price + offset, max_level_price + offset + .01, distance_between_levels)
    orders = [Order(market, side, reduce_only, price, round(get_y_value(slope, y_intercept, price), 3)) for price in prices]

    for order in orders:
        print(order)

    total_order_value = 0
    total_order_size = 0
    for order in orders:
        total_order_value += (order.price * order.size)
        total_order_size += order.size

    print(f'Total order count: {len(orders)}')
    print(f'Total order value ($): {total_order_value}')
    print(f'Total order size ({market}): {total_order_size}')
    return orders
