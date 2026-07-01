from typing import Counter
from factory.factory_info import FactoryInfo
from settings.enviroment import Env


def graph_data(factory_info: FactoryInfo, interval: int):
    data = factory_info.get_data()

    # Extract the individual arrays
    raw_time_array = data[0].astype(int)
    raw_amount_array = data[1]

    # Create the 15-minute interval steps for x axis.
    time_array_list = Env.np.arange(
        raw_time_array.min() // interval,
        raw_time_array.max() // interval + 0.75,
        1,
    )

    # Turn the item into a list of 3.
    # 0 = time, 1 = total item max, 2 = number of machines
    time_array = [[val, 0, []] for val in time_array_list]

    # Add item to the list
    for time, amount in zip(raw_time_array, raw_amount_array):
        check_time = time // interval
        matching_indices = Env.np.where(time_array_list == check_time)[0]

        if len(matching_indices) > 0:
            timeIndex = matching_indices[0]
            time_array[timeIndex][1] += amount
            time_array[timeIndex][2].append(time)

    for item in time_array:
        item_list = item[2]
        counts = Counter(item_list)
        item[2] = counts.most_common(1)[0][1]
    time_array = Env.np.array(time_array)
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


if __name__ == "__main__":
    factory_info = FactoryInfo()
    factory_info.generate_data()
    data_getter(factory_info, 60)
