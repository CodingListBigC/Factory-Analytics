from datetime import datetime, time
from matplotlib.axes import Axes

from factory.time_manger import get_time_list, random_time
from data_generator.data_generator import get_random_list
from settings import config
from settings import enviroment as Env


class Machine:
    start_time: time
    end_time: time
    data = {"time": [], "data": []}

    def __init__(self, start_time: time, end_time: time) -> None:
        self.start_time = start_time  # Start time of machine
        self.end_time = end_time  # End time of machine
        pass

    def isOperation(self, now: datetime) -> bool:
        # Is machine still working at current time
        return self.start_time <= now.time() <= self.end_time

    def generate_data(self) -> None:
        # Generate fake data for testing

        time_list = get_time_list(
            self.start_time, self.end_time
        )  # Create list time need to create data for.
        random_list = get_random_list(time_list)  # Random number for data
        self.data = {"time": time_list, "data": random_list}  # Turn data to real list.
        pass

    def add_points(self, ax: Axes) -> Axes:
        # Add points to plot graph
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

        self.creation_machines()  # Create all of the machines
        pass

    def creation_machines(self) -> None:
        self.machines = []  # Clear list
        for _ in range(self.number_of_machines):
            self.machines.append(
                Machine(random_time(8), random_time(16))
            )  # Create new machine with random time.
        pass

    def generate_data(self) -> None:
        for machine in self.machines:
            machine.generate_data()  # Generate data for each machine
        pass

    def add_points(self, ax: Axes) -> Axes:
        for machine in self.machines:
            ax = machine.add_points(ax)  # Add points to graph
        return ax

    def get_data(self):
        time_array = []
        data_array = []
        for machine in self.machines:
            # Make array for each part
            time = machine.data["time"]
            data = machine.data["data"]

            # Add data to array
            time_array.extend(time)
            data_array.extend(data)

        # Combine data and returns
        return Env.np.vstack((Env.np.array(time_array), Env.np.array(data_array)))

    def __str__(self) -> str:
        return "\n".join(str(machine) for machine in self.machines)


if __name__ == "__main__":
    factoryInfo = FactoryInfo()
    factoryInfo.generate_data()
    print(factoryInfo.get_data())
