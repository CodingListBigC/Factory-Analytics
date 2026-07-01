from typing import Counter
from factory.factory_info import FactoryInfo
from factory.time_manger import number_time
from settings.enviroment import Env


def graph_data(factory_info: FactoryInfo, interval: int):
    data = factory_info.get_data()

    # Extract the individual arrays
    raw_time_array = data[0].astype(int)
    raw_amount_array = data[1]

    # Create the interval steps for x axis.
    time_array_list = Env.np.arange(
        raw_time_array.min() // interval,
        raw_time_array.max() // interval + 0.75,
        1,
    )

    # Turn the item into a temporary python list of lists.
    # 0 = time, 1 = total item max, 2 = number of machines (list to count matches)
    time_list = [[val, 0.0, []] for val in time_array_list]

    # Add items to the list
    for time, amount in zip(raw_time_array, raw_amount_array):
        check_time = time // interval
        matching_indices = Env.np.where(time_array_list == check_time)[0]

        if len(matching_indices) > 0:
            timeIndex = matching_indices[0]
            time_list[timeIndex][1] += amount
            time_list[timeIndex][2].append(time)

    # Condense the list counts
    for item in time_list:
        item_list = item[2]
        if item_list:
            counts = Counter(item_list)
            item[2] = float(counts.most_common(1)[0][1])
        else:
            item[2] = 0.0

    # Extract columns cleanly to avoid object-array math bugs
    times = Env.np.array([item[0] for item in time_list], dtype=float)
    amounts = Env.np.array([item[1] for item in time_list], dtype=float)
    counts = Env.np.array([item[2] for item in time_list], dtype=float)

    # Averages all of the numbers out safely using true float arrays
    averages = Env.np.divide(
        amounts,
        counts,
        out=Env.np.zeros_like(amounts, dtype=float),
        where=counts != 0,
    )

    # Reconstruct a clean numeric array to hand over to the formatter
    time_array = Env.np.column_stack((times, averages))

    return format_time_array(time_array, interval)


def format_time_array(time_array, interval):
    # 1. Scale the time column
    time_array[:, 0] *= interval

    # 2. Convert to a list of formatted 12-hour strings
    formatted_times = []
    for time_int in time_array[:, 0]:
        time_var = number_time(time_int)
        hour = int(time_var[0])
        minute = int(time_var[1])

        # Convert 24-hour to 12-hour format
        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12

        formatted_times.append(f"{hour}:{minute:0>2}")

    # 3. Stack text column alongside the calculated averages float column
    return {"x": formatted_times, "y": time_array[:, 1]}


if __name__ == "__main__":
    factory_info = FactoryInfo()
    factory_info.generate_data()

    # FIXED: Changed data_getter to graph_data to match your function definition
    final_graph_data = graph_data(factory_info, 60)
    print(final_graph_data)
