import pandas as pd

from regulator import Regulator
from sensor import Sensor
from parameters import Parameter


class Controller:
    """Kontroler odpowiadający za współpracę aparatury pomiarowej i regulatora"""

    # Regulator
    _regulator: Regulator
    """Regulator użyty do sterowania"""
    _u_min: float = -5.0
    """Minimalny sygnał reguratora"""
    _u_max: float = 35.0
    """Maksymalny sygnał reguratora"""

    # Sensor
    _sensor: Sensor
    """Czujnik wykonujący pomiary"""
    _val_min: float = 0.0
    """Minimalna wartość pomiaru"""
    _val_max: float = 35.0
    # 2
    """Maksymalna wartość pomiaru"""

    # # Pomieszczenie
    # val_p: float = 0.0
    # """Początkowa wartość regulowanego parametru - temperatury"""
    # val_ust: float = 21.0
    # # 1.5
    # """Docelowa wartość regulowanego parametru - temperatury"""
    #
    # _qd_min: float = 0.0
    # """Minimalne otwarcie zaworu (moc grzejnika)"""
    # _qd_max: float = 1000.0
    # # 0.05
    # """Maksymalne otwarcie zaworu (moc grzejnika)"""

    # Symulacja
    # t_p: float = 0.01
    # """Okres próbkowania [s]"""
    # t_sim: float = 18
    # """Czas symulacji [s]"""
    readings: list = []
    """Lista odczytów"""
    signals: list = []
    """Lista wygnałów sterujących"""
    deviations: list = []
    """Lista uchybów"""
    inputs: list = []
    """Lista wartości 'wpływów' do układu"""

    # # Symulacja 2 - temp
    # u1: float = 2 / 237.15
    # # 1 - 0.2
    # """współczynnik przenikania ciepła przez ściany [W/(m2*K)] -> st.C - na razie podany maxymalny"""
    # u2: float = 0.9 / 273.15
    # """współczynnik przenikania ciepła przez okno [W/(m2*K)] -> st.C - na razie podany maxymalny"""
    # temp_length = 10
    # temp_width = 10
    # temp_height = 3
    # num_window = 1
    # t_outside = 0
    # """temp parametry"""
    # open_wind = 0.2
    # """współczynnik otwarcia okna"""
    # s2: float = 1.6 * 0.5
    # """powierzchnia okna (wymiany ciepła) [m2]"""
    # s1: float = (2 * temp_height*temp_length + 2 * temp_width * temp_height) - (num_window * s2)
    # """powierzchnia ściany (wymiany ciepła) [m2]"""
    # efficiency = 0.8
    # """sprawność urządzenia w przedziale (0; 1)"""

    def __init__(self):
        self._regulator = Regulator(u_min=self._u_min, u_max=self._u_max)
        self._sensor = Sensor(val_min=self._val_min, val_max=self._val_max)

    def make_step(self):
        """Wykonuje jeden krok symulacji (pozycyjnie)"""
        # Oblicz uchyb i dodaj do listy
        deviation = Parameter.val_ust - self.readings[-1]
        self.deviations.append(deviation)

        # # Oblicz wartość sygnału sterującego i dodaj do listy
        # signal = self._regulator.pid_positional(self.deviations, self.t_p)
        # ds = self._regulator.pid_incremental(self.deviations[-1], self.deviations[-2], self.t_p)
        # if self.signals:
        #     signal = self.signals[-1] + ds
        # else:
        #     signal = ds
        signal = self._regulator.pid_positional(self.deviations, Parameter.t_p)
        self.signals.append(signal)

        # # Przekonwertuj sygnał na nastawienie zaworu i dodaj do listy
        input_ = self._signal_to_input(signal)
        self.inputs.append(input_)

        # # Straty ciepła
        wasted = float(
          ((Parameter.u1 * Parameter.s1) + (Parameter.open_wind * Parameter.u2 * Parameter.s2))*(self.readings[-1]-Parameter.t_outside))

        # # Odczytaj aktualny poziom
        reading = self._sensor.read(prev_val=self.readings[-1], q_d=input_, q_s=wasted, t_p=Parameter.t_p)
        self.readings.append(reading)

    def simulate(self):
        """Wykonuje symulację"""
        step_count = Parameter.t_sim / Parameter.t_p
        self.readings = [Parameter.val_p]
        self.deviations = [Parameter.val_ust - Parameter.val_p]
        self.signals = []
        self.inputs = []
        for n in range(0, int(step_count + 1)):
            self.make_step()
        print("Aktualny poziom: ", self.readings)
        print("Uchyb: ", self.deviations)
        print("Sygnał sterujący: ", self.signals)
        print("Nastawienie zaworu: ", self.inputs)

    def _signal_to_input(self, signal: float) -> float:
        """
        Zamienia sygnał otrzymany przez regurator na odpowiedni dopływ do systemu
        :param signal: Sygnał napięciowy otrzymany z regulatora
        :return: dopływ do systemu odpowiadający sygnałowi
        """
        a = (Parameter.qd_max - Parameter.qd_min) / (self._u_max - self._u_min)  # wspolczynnik kierunkowy
        b = Parameter.qd_min - a * self._u_min               # wyraz wolny

        return a * signal + b
        # return self.efficiency * self._qd_max * signal

    def get_simulation_result(self):
        return pd.DataFrame({
            'Krok': range(0, len(self.readings) - 1),
            'Poziom': self.readings[:-1],
            'Sygnaly': self.inputs,
            'Uchyby': self.deviations[:-1]
        })

    @property
    def val_min(self):
        return self._val_min

    @property
    def val_max(self):
        return self._val_max

