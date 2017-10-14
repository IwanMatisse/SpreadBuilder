from Candle import *


def build_spread(list1, list2, factor1, factor2):
    spread = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        candle1 = Candle.from_string(list1[i])
        candle2 = Candle.from_string(list2[j])
        if candle1.is_same_time(candle2):
            spread.append(Candle.make_spread(candle1, factor1, candle2, factor2))
            i += 1
            j += 1
        else:
            if candle2.is_older(candle1):
                j += 1
            else:
                i += 1
        if candle1.filled is False or candle2.filled is False:
            break
    return spread
