
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