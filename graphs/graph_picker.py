from factory import factory_info
from factory.factory_info import FactoryInfo
from graphs import bar_graph, line_graph, plot_graph
from subprocess import call
import os

from menu import menu_master


def main(factory_info: FactoryInfo):
    while True:
        call("clear" if os.name == "posix" else "cls")
        inputs = getInputs()
        match inputs:
            case 0:
                return
            case 1:
                plot_graph.plot_graph(factory_info)
            case 2:
                line_graph.main(factory_info)
            case 4:
                bar_graph.main(factory_info)


options = ["1", "2", "3", "4", "q"]


def getInputs() -> int:
    # 1. Define the options list so .index() has something to search through
    options = ["q", "1", "2", "3", "4"]

    while True:
        menu_master.title("Graph Options")
        print("1: Plot Graph")
        print("2: Line Graph")
        print("3: Plot and Line Graph")
        print("4: Bar Graph")
        print("Q: Exit")

        # .strip() removes any accidental spaces the user might type
        str_input = input("Where do you want to go: ").lower().strip()

        try:
            input_index = options.index(str_input)
            return input_index
        except ValueError:
            print("\n[!] Your input is not one of the options. Please try again.\n")


if __name__ == "__main__":
    factory_info = FactoryInfo()
    factory_info.generate_data()
    main(factory_info)
