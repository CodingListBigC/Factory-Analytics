from factory.factory_info import FactoryInfo
from graphs import graph_picker

# Setup info
factory_info = FactoryInfo()

# Generate Data
factory_info.generate_data()


def main():
    graph_picker.main(factory_info)


if __name__ == "__main__":
    main()
