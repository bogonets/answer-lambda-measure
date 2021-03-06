# -*- coding: utf-8 -*-

import numpy as np
import time
import sys


times = []


def get_fps():
    return len(times)


def add_new(current_time):
    global times
    times.append(current_time)


def remove_old(current_time):
    global times
    times = [x for x in times if current_time - x < 1]


def run():
    cur_t = time.time()
    add_new(cur_t)
    remove_old(cur_t)


def on_run(input):
    run()
    # sys.stdout.write(f"[measure_fps.on_run] FPS : {get_fps()}")
    # sys.stdout.flush()
    return {'fps': str(get_fps())}
