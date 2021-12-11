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

        # # Odczytaj aktualny poziom
        reading = self._sensor.read(prev_val=self.readings[-1], q_d=input_, t_p=Parameter.t_p)
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
        # print("Uchyb: ", self.deviations)
        # print("Sygnał sterujący: ", self.signals)
        # print("Nastawienie zaworu: ", self.inputs)

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

