from datetime import datetime, time
from matplotlib.axes import Axes
import numpy as np


import config
from time_manger import *

np.random.seed(config.RANDOM_SPEED)


class Machine:
    start_time: time
    end_time: time
    data = {"time": [], "data": []}

    def __init__(self, start_time: time, end_time: time) -> None:
        self.start_time = start_time
        self.end_time = end_time
        pass

    def isOperation(self, now: datetime) -> bool:
        if self.start_time <= now.time() and now.time() <= self.end_time:
            return True
        return False

    def generate_data(self) -> None:
        time_list = get_time_list(self.start_time, self.end_time)
        random_list = get_random_list(time_list)
        self.data = {"time": time_list, "data": random_list}
        pass

    def add_points(self, ax: Axes) -> Axes:
        ax.scatter("time", "data", data=self.data)
        return ax

    def __str__(self) -> str:
        return f"Start time: {self.start_time}, End Time: {self.end_time}"

    def __repr__(self) -> str:
        return f"Machine = [Start time: {self.start_time}, End Time: {self.end_time}]"


class FactoryInfo:
    number_of_machines: int
    machines: list[Machine]

    def __init__(self) -> None:
        self.number_of_machines = config.NUMBER_OF_MACHINES

        self.creation_machines()
        pass

    def creation_machines(self) -> None:
        self.machines = []
        for _ in range(self.number_of_machines):
            self.machines.append(Machine(random_time(8), random_time(16)))
        pass

    def generate_data(self) -> None:
        for machine in self.machines:
            machine.generate_data()
        pass

    def add_points(self, ax: Axes) -> Axes:
        for machine in self.machines:
            ax = machine.add_points(ax)
        return ax

    def get_data(self):
        time_array = []
        data_array = []
        for machine in self.machines:
            # Add time to list
            time = machine.data["time"]
            data = machine.data["data"]

            time_array.extend(time)
            data_array.extend(data)

            # Add data to list
        return np.vstack((np.array(time_array), np.array(data_array)))

    def __str__(self) -> str:
        return "\n".join(str(machine) for machine in self.machines)


def get_random_list(times) -> list[int]:
    times = np.array(times)
    curve_baseline = np.zeros_like(times, dtype=float)

    t_min = times.min()
    t_max = times.max()
    total_duration = t_max - t_min

    # 1. Subtle, expanded milestones
    # Start-up is the first 15% of the shift, clean-up is the last 15%
    startup_end = t_min + (total_duration * 0.15)
    lunch_start = t_min + (total_duration * 0.40)
    lunch_end = t_min + (total_duration * 0.60)
    cleanup_start = t_min + (total_duration * 0.85)

    for i, t in enumerate(times):
        if t < startup_end:
            # Start-up phase: Gentle ramp up from 15 to 40
            pct = (
                (t - t_min) / (startup_end - t_min) if (startup_end - t_min) > 0 else 1
            )
            curve_baseline[i] = 15 + (40 - 15) * pct

        elif startup_end <= t < lunch_start:
            # Morning Peak: Steady high efficiency
            curve_baseline[i] = 40.0

        elif lunch_start <= t < (lunch_start + (lunch_end - lunch_start) / 2):
            # Heading into lunch: Subtle drop from 40 down to 20 (instead of -10)
            mid_lunch = lunch_start + (lunch_end - lunch_start) / 2
            pct = (t - lunch_start) / (mid_lunch - lunch_start)
            curve_baseline[i] = 40 - (40 - 20) * pct

        elif (lunch_start + (lunch_end - lunch_start) / 2) <= t < lunch_end:
            # Post-lunch recovery: Gentle return from 20 back up to 40
            mid_lunch = lunch_start + (lunch_end - lunch_start) / 2
            pct = (t - mid_lunch) / (lunch_end - mid_lunch)
            curve_baseline[i] = 20 + (40 - 20) * pct

        elif lunch_end <= t < cleanup_start:
            # Afternoon Peak: Steady high production
            curve_baseline[i] = 40.0

        else:
            # Clean-up phase: Drop from 40 down to a resting 15 (instead of 0)
            pct = (
                (t - cleanup_start) / (t_max - cleanup_start)
                if (t_max - cleanup_start) > 0
                else 1
            )
            curve_baseline[i] = 40 - (40 - 15) * pct

    # 2. Lower the noise scale so individual points don't jump around wildly
    noise = np.random.normal(loc=0.0, scale=1.0, size=len(times))
    generated_amounts = curve_baseline + noise

    return np.round(generated_amounts).astype(int).tolist()


if __name__ == "__main__":
    factoryInfo = FactoryInfo()
    factoryInfo.generate_data()
    print(factoryInfo.get_data())
