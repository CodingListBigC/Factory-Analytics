from factory.factory_info import FactoryInfo
from graphs.plot_graph import plot_graph
from graphs import line_graph

# Setup info
factory_info = FactoryInfo()

# Generate Data
factory_info.generate_data()


def main():
    plot_graph(factory_info)
    line_graph.main(factory_info)


if __name__ == "__main__":
    main()
