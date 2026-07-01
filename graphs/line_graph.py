from data_generator.data_getter import graph_data
from settings.enviroment import Env
from factory.factory_info import FactoryInfo


def show_data(x, y):
    # Show data as a line graph
    fig, ax = Env.plt.subplots()
    ax.plot(x, y, label="Average items made")
    Env.plt.legend()
    Env.plt.show()


def main(factory_info: FactoryInfo):
    final_array = graph_data(factory_info, 60)

    x = final_array[:, 0].tolist()
    y = final_array[:, 1].tolist()

    show_data(x, y)

    final_array = graph_data(factory_info, 15)

    x = final_array[:, 0].tolist()
    y = final_array[:, 1].tolist()

    show_data(x, y)


if __name__ == "__main__":
    factory_info = FactoryInfo()
    factory_info.generate_data()

    main(factory_info)
