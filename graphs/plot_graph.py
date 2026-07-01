from settings.enviroment import Env
from factory.factory_info import FactoryInfo


def plot_graph(factory_info: FactoryInfo):
    fig, ax = Env.plt.subplots(figsize=(5, 2.7), layout="constrained")
    ax = factory_info.add_points(ax)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amount of item made")

    Env.plt.show()


if __name__ == "__main__":
    print("Show plot graph")
    factory_info = FactoryInfo()
    factory_info.generate_data()

    plot_graph(factory_info)
