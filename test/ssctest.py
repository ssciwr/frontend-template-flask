# !/usr/bin/env python
import math
import time
import json
import os
import random
import string


def circle_area(radius):
    return math.pi * radius * radius


def timing_task(length):
    print("Printed immediately.")
    time.sleep(5)
    print("Printed after 5 seconds.")
    return length * length * length


def test_json():
    with open("../statics/json/input.json", "r") as load_f:
        input = json.load(load_f)

    print(input)

    path = "../statics/json/cache/"
    if not os.path.exists(path):
        os.makedirs(path)

    with open("../statics/json/cache/input.json", "w") as dump_f:
        json.dump(input, dump_f, indent=4)


def test_random_str():
    print(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()'))
    print(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    print(''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 15)))
    print(''.join(random.sample('abcdefghijklmnopqrstuvwxyz!0123456789', 25)))











