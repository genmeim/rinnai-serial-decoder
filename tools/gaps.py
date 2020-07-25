#!/usr/bin/python

test_bits_length = 4

HEAD_WIDTH = 700
GAP_WIDTH = 150
BIT_WIDTH = 450

for num in range(pow(2, test_bits_length)):

    total_width = HEAD_WIDTH
    last_bit = 1
    print("{:5d}".format(num), " ", end="")

    for bit in range(test_bits_length - 1, -1, -1):

        next_bit = 1 if (num & pow(2, bit) == pow(2, bit)) else 0

        # H > H : +GAP
        if last_bit == 1 and next_bit == 1:
            total_width += GAP_WIDTH
        # L > L : +GAP
        if last_bit == 0 and next_bit == 0:
            total_width += GAP_WIDTH
        # L > H : +2GAPs
        if last_bit == 0 and next_bit == 1:
            total_width += GAP_WIDTH * 2

        # H > L : No GAPs

        total_width += BIT_WIDTH
        last_bit = next_bit
        print(next_bit, end="")

    # all bit's process done, back to LO signal level.
    # L > L : +GAP
    if last_bit == 0:
        total_width += GAP_WIDTH
    print("  w:", total_width, "uSec")

print("done.")
