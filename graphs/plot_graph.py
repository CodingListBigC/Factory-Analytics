from factory.time_manger import number_time
from settings.enviroment import Env
from factory.factory_info import FactoryInfo


def plot_graph(factory_info: FactoryInfo):
    fig, ax = Env.plt.subplots(
        figsize=(10, 5), layout="constrained"
    )  # Made wider to fit nicely

    raw_data = factory_info.get_data()
    time_data_dict = format_time_array(raw_data, 1)

    # Plot the data points
    ax.scatter("x", "y", data=time_data_dict, alpha=0.7)

    ax.set_xlabel("Time")
    ax.set_ylabel("Amount of item made")

    # Get ONLY the unique labels for setting tick intervals
    unique_labels = list(dict.fromkeys(time_data_dict["x"]))

    # Show every 4th unique time label on the axis
    tick_positions = list(range(0, len(unique_labels), 4))
    tick_labels = unique_labels[::4]

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)

    # Rotate labels slightly so they never overlap

    ax.grid(True, linestyle="--", alpha=0.5)
    Env.plt.show()


def format_time_array(time_array, interval):
    # 1. Scale the time column
    time_array[:, 0] *= interval

    # 2. Find unique times and group the amounts
    unique_times = Env.np.unique(time_array[:, 0])

    formatted_times = []
    y_values = []

    for t in unique_times:
        # Format the unique time string
        time_var = number_time(t)
        hour = int(time_var[0])
        minute = int(time_var[1])

        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12

        formatted_str = f"{hour}:{minute:0>2}"

        # Get all y-values matching this specific timestamp
        matching_y = time_array[time_array[:, 0] == t, 1]

        for val in matching_y:
            formatted_times.append(formatted_str)
            y_values.append(float(val))

    return {"x": formatted_times, "y": y_values}


if __name__ == "__main__":
    print("Show plot graph")
    factory_info = FactoryInfo()
    factory_info.generate_data()

    plot_graph(factory_info)
