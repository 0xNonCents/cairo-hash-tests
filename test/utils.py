from ast import Call
from typing import Callable, List, Tuple, Any, NamedTuple
from functools import reduce
from enum import Enum

shift = 2 ** 128
all_ones = 2 ** 128 - 1
def toUint256(num : int):
    low = num & all_ones
    high = (num << 128) & all_ones

    return (low, high)

shift_256 = 2 ** 256
all_ones_256 = 2 ** 256 - 1

def splitToTwoUint256(num : int):
    low = toUint256(num & all_ones_256)
    mid = toUint256((num << 256) & all_ones_256)
    high = toUint256((num << 512) & all_ones_256)

    return (low, mid, high)

def fromUint256(num):
    return num.low + num.high * shift


class Encoding(Enum):
    LITTLE: str = 'little'
    BIG: str = 'big'

concat_arr: Callable[[List[str]], str] = lambda arr: reduce(lambda a, b: a + b, arr)

def bytes_to_int(word: bytes, encoding: Encoding = Encoding.BIG) -> int:
    return int.from_bytes(word, encoding.value)

bytes_to_int_little: Callable[[bytes], int] = lambda word: int.from_bytes(word, "little")
bytes_to_int_big: Callable[[bytes], int] = lambda word: int.from_bytes(word, "big")

int_to_uint_256 : Callable[[int], tuple] = lambda word : toUint256(word)