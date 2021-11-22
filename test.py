from controller import Controller
from matplotlib import pyplot as plt


def run():
    """Wykonuje kod w ramach testów"""
    c = Controller()
    c.simulate()

    # plotting
    x = range(0, len(c.readings)-1)

    fig, axs = plt.subplots(3)
    axs[0].plot(x, c.readings[:-1])
    axs[1].plot(x, c.inputs)
    axs[2].plot(x, c.signals)

    plt.show()

    print("")
