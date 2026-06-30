from factory_info import FactoryInfo
from environment import Env


def get_graph_data(factory_info: FactoryInfo):
    data = factory_info.get_data()

    # Extract the individual arrays
    raw_time_array = data[0].astype(int)
    raw_amount_array = data[1]

    # Create the 15-minute interval steps for x axis.
    time_array_list = Env.np.arange(raw_time_array.min(), raw_time_array.max() + 1, 15)

    # Turn the item into a list of 3.
    # 0 = time, 1 = total item max, 2 = number of machines
    time_array = Env.np.zeros((len(time_array_list), 3), dtype=float)
    time_array[:, 0] = time_array_list

    # Add item to the list
    for time, amount in zip(raw_time_array, raw_amount_array):
        matching_indices = Env.np.where(time_array_list == time)[0]

        if len(matching_indices) > 0:
            timeIndex = matching_indices[0]
            time_array[timeIndex, 1] += amount
            time_array[timeIndex, 2] += 1

    # Averages all of the numbers out
    averages = Env.np.divide(
        time_array[:, 1],
        time_array[:, 2],
        out=Env.np.zeros_like(time_array[:, 1], dtype=float),
        where=time_array[:, 2] != 0,
    )

    # Add them back in
    time_array[:, 1] = averages

    return time_array


def show_data(x, y):
    # Show data as a line graph
    fig, ax = Env.plt.subplots()
    ax.plot(x, y, label="Average items made")
    Env.plt.legend()
    Env.plt.show()


def main(factory_info: FactoryInfo):
    final_array = get_graph_data(factory_info)

    x = final_array[:, 0].tolist()
    y = final_array[:, 1].tolist()

    show_data(x, y)


if __name__ == "__main__":
    factory_info = FactoryInfo()
    factory_info.generate_data()

    main(factory_info)
