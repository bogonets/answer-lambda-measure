# -*- coding: utf-8 -*-

import numpy as np
import time
import sys


TRUE_STR_LIST = ['true']

maximum_sec = 0
seconds = [1]
labels = ['Occur1']
measure_counts = [0.5]
alarm_interval_seconds = [1]

input_times = []
states = []
next_alarm_times = []

cache_input = None

input_fps = []

always_out = False

PROPS_NAME_SECONDS = "seconds"
PROPS_NAME_LABELS = "labels"
PROPS_NAME_MEASURE_COUNT = "measure_ratio"
PROPS_NAME_ALARM_INTERVAL_SECONDS = "alarm_interval_seconds"
PROPS_NAME_ALWAYS_OUT = "always_out"

FPS_EXPIRED_COUNT = 10


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
        measure_counts = [float(i) for i in v.split(',')]
    elif k == PROPS_NAME_ALARM_INTERVAL_SECONDS:
        global alarm_interval_seconds
        alarm_interval_seconds = [int(i) for i in v.split(',')]
    elif k == PROPS_NAME_ALWAYS_OUT:
        global always_out
        always_out = True if v.lower() in TRUE_STR_LIST else False


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
    elif k == PROPS_NAME_ALWAYS_OUT:
        return str(always_out)


def on_init():
    return initialize_variables()


def on_run(array, fps):

    # sys.stderr.write(f"[measure_adaptive_run] array : {array}\n")
    # sys.stderr.write(f"[measure_adaptive_run] array.shape : {array.shape}\n")
    # sys.stderr.write(f"[measure_adaptive_run] fps : {fps}\n")
    # sys.stderr.flush()

    fps_value = int(''.join([chr(x) for x in fps]))
    # sys.stderr.write(f"[measure_adaptive_run] fps_value : {fps_value} / {type(fps_value)}\n")
    # sys.stderr.flush()

    add_fps(fps_value)
    if not remove_expired_fps(FPS_EXPIRED_COUNT):
        return returnValue()
    mean_fps = get_mean_fps()

    # current_time.
    cur_t = time.time()

    if not check_valid_props():
        sys.stderr.write(
            "[measure_per_time.on_run] states is empty. Because props is invalid value.\n")
        sys.stderr.flush()
        return returnValue()

    remove_expired(cur_t)

    # Check input is not empty.
    if array.shape:
        # sys.stdout.write("[measure_per_time_adaptive.on_run] input!!")
        # sys.stdout.flush()

        update_cache(array)
        add_new_time(cur_t)

    measure_state(cur_t, mean_fps)

    alarms = measure_alarm(cur_t)
    if len(alarms) == 0:
        return returnValue()
    alarm_labels = ','.join([labels[x] for x in alarms])

    # sys.stderr.write(f"[measure_adaptive.on_run] alarm_labels : {alarm_labels}.\n")
    # sys.stderr.flush()
    if alarm_labels:
        return {
            'result': cache_input,
            'labels': alarm_labels
        }
    else:
        return returnValue()


def on_destroy():
    return True


def returnValue():
    if always_out:
        return {
            'result': None,
            'labels': None
        }
    else:
        return {}


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
    # filtered = list(filter(lambda x: current - x <= sec, input_times))
    filtered = [x for x in input_times if current - x <= sec]
    return len(filtered) >= count


def active(idx):
    global states
    states[idx] = True


def deactive(idx):
    global states
    states[idx] = False
    next_alarm_times[idx] = 0
    reset_cache()


def measure_state(cur_t, mean_fps):

    if not input_times:
        return False

    for idx, items in enumerate(zip(seconds, measure_counts)):
        sec, mcount = items

        compare_count = sec * mean_fps * mcount

        if is_active(cur_t, sec, compare_count):
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


# FPS functions
def add_fps(fps):
    global input_fps
    input_fps.append(fps)


def remove_expired_fps(expired_count):
    global input_fps
    for i in range(len(input_fps) - 10):
        input_fps.pop(0)
    # sys.stdout.write(f"[measure_per_time_adaptive.remove_expired_fps] input_fps len : {len(input_fps)}\n")
    # sys.stdout.write(f"[measure_per_time_adaptive.remove_expired_fps] expired_count : {expired_count}\n")
    # sys.stdout.flush()
    return len(input_fps) == expired_count


def get_mean_fps():
    return sum(input_fps) / len(input_fps)
