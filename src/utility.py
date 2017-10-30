import random

def reduceNumber(number, divisor):
    result = number // divisor
    mod = number % divisor
    if random.random() < (mod / divisor):
        result += 1
    return result

def lerp(start, end, mix):
    return start + (end - start)*mix

def incSpeedLerp(start, end, mix):
    return lerp(start, end, mix**2)

def decSpeedLerp(start, end, mix):
    return lerp(start, end, 1 - (1 - mix)**2)

def incDecSpeedLerp(start, end, mix):
    midpoint = lerp(start, end, 0.5)
    if mix < 0.5:
        return incSpeedLerp(start, midpoint, mix*2)
    else:
        return decSpeedLerp(midpoint, end, (mix - 0.5)*2)

def decIncSpeedLerp(start, end, mix):
    midpoint = lerp(start, end, 0.5)
    if mix < 0.5:
        return decSpeedLerp(start, midpoint, mix*2)
    else:
        return incSpeedLerp(midpoint, end, (mix - 0.5)*2)
