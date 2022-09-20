from math import cos, pi as PI
from random import randint

def get_spread_random_value(rng=None) -> float:
	rng = randint if rng is None else rng.randint
	value = rng(0, 1000) / 1000
	curve = lambda x: abs(pow(min(cos(PI * x / 2.0), 1.0 - abs(x)), 3.0))
	out_unclamped = curve(value)
	out_inv = 1 - out_unclamped
	out_clamped = max(min(out_inv, 1), 0)

	return out_clamped

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)