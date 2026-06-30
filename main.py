import numpy as np

import matplotlib

from factory_info import FactoryInfo


matplotlib.use("qtagg")

import matplotlib.pyplot as plt

np.array(3)

# Setup info
factory_info = FactoryInfo()

# Generate Data
factory_info.generate_data()


def plot_graph(factory_info: FactoryInfo):
    fig, ax = plt.subplots(figsize=(5, 2.7), layout="constrained")
    ax = factory_info.add_points(ax)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amount of item made")

    plt.show()


def graph_data(factory_info: FactoryInfo):
    data = factory_info.get_data()

    # Extract the individual arrays
    raw_time_array = data[0].astype(int)
    raw_amount_array = data[1]

    # Create the 15-minute interval steps
    time_array_list = np.arange(raw_time_array.min(), raw_time_array.max() + 1, 15)

    # Initialize matrix as float from the start to handle decimals later
    time_array = np.zeros((len(time_array_list), 3), dtype=float)
    time_array[:, 0] = time_array_list

    # Correctly loop through each individual time and amount pair
    for time, amount in zip(raw_time_array, raw_amount_array):
        # Match individual integer times
        matching_indices = np.where(time_array_list == time)[0]

        if len(matching_indices) > 0:
            timeIndex = matching_indices[0]
            time_array[timeIndex, 1] += amount
            time_array[timeIndex, 2] += 1

    # Safely compute averages
    averages = np.divide(
        time_array[:, 1],
        time_array[:, 2],
        out=np.zeros_like(time_array[:, 1], dtype=float),
        where=time_array[:, 2] != 0,
    )

    # Overwrite column 1 with averages
    time_array[:, 1] = averages

    # Slice to keep only columns 0 and 1 (effectively deleting column 2)
    final_array = time_array[:, :2]

    np.set_printoptions(suppress=True, precision=2)

    x = final_array[:, 0].tolist()
    y = final_array[:, 1].tolist()
    fig, ax = plt.subplots()  # Create a figure containing a single Axes.
    ax.plot(x, y)  # Plot some data on the Axes.
    plt.show()


# Graph Type
graph_data(factory_info)
