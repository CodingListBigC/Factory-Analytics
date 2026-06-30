from datetime import time
import numpy as np


def random_time(start_hour: int) -> time:
    random_mintue = np.random.choice([-30, -15, 0, 15, 30])
    if random_mintue < 0:
        start_hour -= 1
        random_mintue += 60
    return time(start_hour, random_mintue)


def get_time_list(start_time: time, end_time: time) -> list[int]:
    array = []
    for hour in range(start_time.hour, end_time.hour + 1):
        start_min = start_time.minute if hour == start_time.hour else 0
        end_min = end_time.minute if hour == end_time.hour else 60

        for minute in range(start_min, end_min, 15):
            array.append(time_to_number(hour, minute))
    return array


def time_to_number(hour: int, minute: int) -> int:
    return (hour * 60) + (minute)


def number_time(time: int):
    return [time // 60, time % 60]
