from controller import Controller
from matplotlib import pyplot as plt


def run():
    """Wykonuje kod w ramach testów"""
    c = Controller()
    c.simulate()
    cds = c.get_simulation_result()

    # plotting
    x = cds['Krok']

    fig, axs = plt.subplots(3)
    axs[0].plot(x, cds['Poziom'])
    axs[1].plot(x, cds['Sygnaly'])
    axs[2].plot(x, cds['Uchyby'])

    plt.show()

    print("")
