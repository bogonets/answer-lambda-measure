# -*- coding: utf-8 -*-

import numpy as np
import time
import sys

maximum = 0
seconds = [1]
labels = ['Occur1']
estimation_count = [1]
interval_sec = [1]

last_estimated_times = []
input_times = []


def on_set(k, v):
    if k == "seconds":
        global seconds
        global longest
        seconds = [int(i) for i in v.split(',')]
        maximum = max(seconds)
    elif k == "labels":
        global labels
        labels = v.split(',')
    elif k == "estimation_count":
        global estimation_count
        estimation_count = [int(i) for i in v.split(',')]
    elif k == "":
        global estimation_count
        estimation_count = [int(i) for i in v.split(',')]


def on_get(k):
    if k == "seconds":
        s = [str(i) for i in seconds]
        return ','.join(s)
    elif k == "labels":
        return ','.join(labels)
    elif k == "estimation_count":
        return str(estimation_count)


def put_new_time(t):
    global input_times
    input_times.append(t)


def estimate_in_time(cur_t):

    estimated = [[]] * len(seconds)

    # 전체
    for t in input_times:
        dt = cur_t - t

        for idx, s in enumerate(seconds):
            if s <= dt:
                estimated[idx].append(t)

    return estimated


def estimate_out(cur_t, estimated):
    global last_estimated_times

    result_labels = [None] * len(seconds)

    dtimes = [cur_t - i for i in last_estimated_times]

    for idx, e in enumerate(estimated):
        if dtimes[idx] < interval_sec[idx]:
            continue
        else:
            if len(e) >= estimation_count[idx]:
                last_estimated_times[idx] = cur_t
                result_labels[idx] = labels[idx]

    return result_labels


def on_run(array):

    # cur_time.
    cur_t = time.time()

    # Input new one.
    put_new_time(cur_t)

    # Estimate in time.
    estimated = estimate_in_time(cur_t)

    # Estimate result.
    result_labels = estimate_out(cur_t, estimated)

    # Filter
    result_labels = [l for l in result_labels if l is not None]

    condition_result = 0 if len(result_labels) == 0 else 1

    return {
        'condition': np.array([condition_result], np.int32),
        'labels': np.array()
    }


def on_destroy():
    return True
