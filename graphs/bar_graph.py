import os
from subprocess import call

from data_generator.data_getter import format_time_array, graph_data
from factory import factory_info
from factory.factory_info import FactoryInfo
from menu import menu_master
from settings.enviroment import Env


def main(factory_info: FactoryInfo):
    print("Main")
    while True:
        call("clear" if os.name == "posix" else "cls")
        input = pick_options()
        match input:
            case 0:
                return
            case 1:
                time_graph(factory_info, 0)
            case 2:
                time_graph(factory_info, 1)
            case 3:
                adverage_items(factory_info, 60)
            case 4:
                adverage_items(factory_info, 15)


def pick_options():
    options = ["q", "1", "2", "3", "4"]
    while True:
        menu_master.title("Bar Graph Options")
        print("1:Start Time")
        print("2: End Time")
        print("3: Item made per hour")
        print("4: Item made per fifteen")
        print("Q: Exit")

        # .strip() removes any accidental spaces the user might type
        str_input = input("Where do you want to go: ").lower().strip()
        try:
            input_index = options.index(str_input)
            return input_index
        except ValueError:
            print("\n[!] Your input is not one of the options. Please try again.\n")


def time_graph(factory_info: FactoryInfo, type: int):
    if type > 1 or type < 0:
        type = 0

    time_array_list_raw = factory_info.get_item_list(type)
    time_array_list = Env.np.unique(time_array_list_raw)

    time_array = Env.np.zeros((len(time_array_list), 2), dtype=float)
    time_array[:, 0] = time_array_list

    for time in time_array_list_raw:
        matching_indices = Env.np.where(time_array_list == time)[0]

        if len(matching_indices) > 0:
            timeIndex = matching_indices[0]
            time_array[timeIndex, 1] += 1

    time_array = format_time_array(time_array, 1)

    x = time_array["x"]
    y = time_array["y"]

    fig, ax = Env.plt.subplots(figsize=(5, 2.7), layout="constrained")

    ax.bar(x, y)
    ax.set_xlabel(f"{'Start' if type == 0 else 'End'} Time")
    ax.set_ylabel(f"Number of machine {'activated' if type == 0 else 'deactivated'}")
    if len(x) > 8:
        ax.set_xticks(x[::2])
        ax.set_xticklabels(x[::2])

    Env.plt.show()


def adverage_items(factory_info: FactoryInfo, interval: int):
    data = graph_data(factory_info, interval)

    x = data["x"]
    y = data["y"]

    fig, ax = Env.plt.subplots(figsize=(5, 2.7), layout="constrained")

    ax.bar(x, y)
    ax.set_xlabel("Time")
    ax.set_ylabel("Items Made")
    if len(x) > 8:
        ax.set_xticks(x[::2])
        ax.set_xticklabels(x[::2])

    Env.plt.show()


if __name__ == "__main__":
    factory_info = FactoryInfo()
    factory_info.generate_data()

    main(factory_info)
