from dataclasses import dataclass


@dataclass
class Order:
    market: str
    side: str
    reduce_only: bool
    price: float
    size: float


@dataclass
class Input:
    market: str
    side: str
    reduce_only: bool
    min_level_price: float
    min_level_size: float
    max_level_price: float
    max_level_size: float
    distance_between_levels: float
    offset: float
