# -*- coding: utf-8 -*-

import numpy as np
import time
import sys
from datetime import datetime


maximum_sec = 0
seconds = [1]
labels = ['Occur1']
measure_counts = [1]
alarm_interval_seconds = [1]

input_times = []
states = []
next_alarm_times = []

cache_input = None

PROPS_NAME_SECONDS = "seconds"
PROPS_NAME_LABELS = "labels"
PROPS_NAME_MEASURE_COUNT = "measure_counts"
PROPS_NAME_ALARM_INTERVAL_SECONDS = "alarm_interval_seconds"


def on_set(k, v):
    if k == PROPS_NAME_SECONDS:
        global seconds
        global maximum_sec
        seconds = [int(i) for i in v.split(',')]
        maximum_sec = max(seconds)
    elif k == PROPS_NAME_LABELS:
        global labels
        labels = v.split(',')
    elif k == PROPS_NAME_MEASURE_COUNT:
        global measure_counts
        measure_counts = [int(i) for i in v.split(',')]
    elif k == PROPS_NAME_ALARM_INTERVAL_SECONDS:
        global alarm_interval_seconds
        alarm_interval_seconds = [int(i) for i in v.split(',')]


def on_get(k):
    if k == PROPS_NAME_SECONDS:
        s = [str(i) for i in seconds]
        return ','.join(s)
    elif k == PROPS_NAME_LABELS:
        return ','.join(labels)
    elif k == PROPS_NAME_MEASURE_COUNT:
        c = [str(i) for i in measure_counts]
        return ','.join(c)
    elif k == PROPS_NAME_ALARM_INTERVAL_SECONDS:
        c = [str(i) for i in alarm_interval_seconds]
        return ','.join(c)


def on_init():
    return initialize_variables()


def on_run(input):
    # sys.stdout.write(f"[measure_per_time.on_run] input1: {input}\n")
    # sys.stdout.flush()

    # current_time.
    cur_t = time.time()

    if not check_valid_props():
        sys.stderr.write(
            "[measure_per_time.on_run] states is empty. Because props is invalid value.\n")
        return {}

    # sys.stdout.write(f"[measure_per_time.on_run] input2: {input}\n")
    # sys.stdout.flush()
    remove_expired(cur_t)

    # sys.stdout.write(f"[measure_per_time.on_run] input3: {input}\n")
    # sys.stdout.flush()
    if len(input) != 0:
        update_cache(input)
        add_new_time(cur_t)
    # sys.stdout.write(f"[measure_per_time.on_run] input4: {input}\n")
    # sys.stdout.flush()
    measure_state(cur_t)
    # sys.stdout.write(f"[measure_per_time.on_run] input5: {input}\n")
    # sys.stdout.flush()
    alarms = measure_alarm(cur_t)

    # sys.stdout.write(f"[measure_per_time.on_run] alarms6: {alarms}\n")
    # sys.stdout.flush()
    if len(alarms) == 0:
        return {}

    # sys.stdout.write(f"[measure_per_time.on_run] input7: {input}\n")
    # sys.stdout.flush()

    # now = datetime.now()
    # dt = now.strftime("%m/%d/%Y, %H:%M:%S")
    # sys.stdout.write(f"[measure_per_time.on_run] time: {dt}\n")
    # sys.stdout.flush()

    # sys.stdout.write(f"[measure_per_time.on_run] result: {cache_input}\n")
    # sys.stdout.write(f"[measure_per_time.on_run] labels: {alarms}\n")
    # sys.stdout.write(f"[measure_per_time.on_run] result's lables: {[labels[x] for x in alarms]}\n")
    # sys.stdout.flush()

    alarm_labels = np.zeros([len(alarms), len(max(labels))], dtype=np.uint8)

    return {
        'result': cache_input,
        'labels': alarm_labels
    }


def on_destroy():
    return True


def initialize_variables():
    global states
    global next_alarm_times
    if not check_valid_props():
        return False
    states = [False] * len(seconds)
    next_alarm_times = [0] * len(seconds)
    return True


def check_valid_props():
    return len(seconds) == len(labels) == len(measure_counts)


def remove_expired(current):
    global input_times
    input_times = list(
        filter(lambda x: current - x < maximum_sec, input_times))


def add_new_time(t):
    global input_times
    input_times.append(t)


def update_cache(v):
    global cache_input
    cache_input = v


def reset_cache():
    global cache_input
    cache_input = None


def is_active(current, sec, count):
    filtered = list(filter(lambda x: current - x <= sec, input_times))
    return len(filtered) >= count


def active(idx):
    states[idx] = True


def deactive(idx):
    states[idx] = False
    next_alarm_times[idx] = 0
    reset_cache()


def measure_state(cur_t):

    if not input_times:
        return False

    for idx, items in enumerate(zip(seconds, measure_counts)):
        sec, mcount = items

        if is_active(cur_t, sec, mcount):
            active(idx)
        else:
            deactive(idx)


def measure_alarm(current):
    alarm_idxes = []
    for idx, items in enumerate(zip(states, alarm_interval_seconds, next_alarm_times)):
        state, interval, next_time = items

        if not state:
            continue

        if next_time == 0:
            next_alarm_times[idx] = current
            alarm_idxes.append(idx)
            continue

        dt = current - next_time

        if dt >= interval:
            alarm_idxes.append(idx)
            next_alarm_times[idx] += interval
    return alarm_idxes
