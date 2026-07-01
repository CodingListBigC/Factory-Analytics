import os
from subprocess import call

from matplotlib.ticker import MaxNLocator
from data_generator.data_getter import graph_data
from menu import menu_master
from settings.enviroment import Env
from factory.factory_info import FactoryInfo


def show_data(x, y):
    # Show data as a line graph
    fig, ax = Env.plt.subplots()
    ax.plot(x, y, label="Average items made")
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
    Env.plt.legend()
    Env.plt.show()


def main_all(factory_info: FactoryInfo):
    final_array = graph_data(factory_info, 60)

    x = final_array["x"]
    y = final_array["y"]

    show_data(x, y)

    final_array = graph_data(factory_info, 15)

    x = final_array["x"]
    y = final_array["y"]

    show_data(x, y)


def main(factory_info: FactoryInfo):
    while True:
        call("clear" if os.name == "posix" else "cls")
        input = pick_options()
        match input:
            case 0:
                return
            case 1:
                adverage(factory_info, 60)
            case 2:
                adverage(factory_info, 15)


def pick_options():
    options = ["q", "1", "2"]
    while True:
        menu_master.title("Line Graph Options")
        print("1: Adverage item made per hour")
        print("2: Adverage item made per fifteen")
        print("Q: Exit")

        # .strip() removes any accidental spaces the user might type
        str_input = input("Where do you want to go: ").lower().strip()
        try:
            input_index = options.index(str_input)
            return input_index
        except ValueError:
            print("\n[!] Your input is not one of the options. Please try again.\n")


def adverage(factory_info: FactoryInfo, interval: int):
    print("Showing adverage: ", interval)
    final_array = graph_data(factory_info, interval)

    x = final_array["x"]
    y = final_array["y"]

    show_data(x, y)


if __name__ == "__main__":
    factory_info = FactoryInfo()
    factory_info.generate_data()

    main(factory_info)
