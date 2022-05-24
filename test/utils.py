from ast import Call
from typing import Callable, List, Tuple, Any, NamedTuple
from functools import reduce
from enum import Enum


def split(num: int, num_bits_shift: int = 128, length: int = 3) -> List[int]:
    a = []
    for _ in range(length):
        a.append( num & ((1 << num_bits_shift) - 1) )
        num = num >> num_bits_shift 
    return tuple(a)

shift = 2 ** 128
all_ones = 2 ** 128 - 1

def toUint256(num : int):
    low = num & all_ones
    high = (num << 128) & all_ones

    return (low, high)

shift_256 = 2 ** 256
all_ones_256 = 2 ** 256 - 1

def splitUint768(num : int):
    low = toUint256(num & all_ones_256)
    mid = toUint256((num << 256) & all_ones_256)
    high = toUint256((num << 512) & all_ones_256)

    return [low, mid, high]

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

int_to_uint_256 : Callable[[int], tuple] = lambda word : split(word, 128, 2)

int_to_bytes_32_big : Callable[[int], bytes] = lambda word: word.to_bytes(32, "big")

bytes_32_to_uint_256 : Callable[[bytes], tuple] = lambda word : split(bytes_to_int_big(word), 128, 2)

def bytes_to_uint256(input : bytes, bytes_per_uint256 : int = 32):
    length_of_bytes = len(input)

    total_chunks, loose_bytes = divmod(length_of_bytes ,bytes_per_uint256 )
    chunks = []
    for x in range(total_chunks):
        if x == 0:
            chunks.append(bytes_32_to_uint_256(input[:32]))
        else:
            chunks.append(bytes_32_to_uint_256(input[(x - 1) * 32 : x * 32]))
    if loose_bytes > 0:
        chunks.append(bytes_32_to_uint_256(input[total_chunks * bytes_per_uint256:]))
    return chunks

def pad_bytes(input : bytes, bytes_per_uint256 : int = 32):
    length_of_bytes = len(input)
    
    missing_bytes = bytes_per_uint256 - length_of_bytes
    
    if missing_bytes == 1:
        return input + b'\x86'
    elif missing_bytes == 2:
        return input + b'\x06\x80'
    
    
    for x in range(missing_bytes):
        if x == 0 :
            input = input + b'\x06'
        elif x == missing_bytes:
            input = input + b'\x80'
        else:
            input = input + b'\x00'
    
    return input



def bytes_as_int_arr(input : bytes, bytes_per_int : int = 8):

    a = []
    input_length = len(input)
    chunks, extra = divmod(input_length, bytes_per_int)

    for x in range(chunks):
        if x == 0:
            a.append(bytes_to_int_little(input[:bytes_per_int]))
        else:
            a.append(bytes_to_int_little(input[x * bytes_per_int : (x + 1) * bytes_per_int]))
    
    if extra > 0:
        min = chunks * bytes_per_int
        max = chunks * bytes_per_int + extra

        a.append(bytes_to_int_little(input[min : max]))

    return a