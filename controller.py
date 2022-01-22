import pandas as pd
from numpy import arange

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

    params: Parameter

    readings: list = []
    """Lista odczytów"""
    signals: list = []
    """Lista wygnałów sterujących"""
    deviations: list = []
    """Lista uchybów"""
    inputs: list = []
    """Lista wartości 'wpływów' do układu"""

    energy_ins: list = []
    energy_ins_sums: list = []
    """Energia dostarczona do układu"""
    energy_outs: list = []
    energy_outs_sums: list = []
    """Energia dostarczona do układu"""

    def __init__(self):
        self.params = Parameter()
        self._regulator = Regulator(params=self.params)
        self._sensor = Sensor(params=self.params)

    def make_step(self):
        """Wykonuje jeden krok symulacji (przyrostowo)"""
        # Oblicz uchyb i dodaj do listy
        deviation = self.params.val_ust - self.readings[-1]
        self.deviations.append(deviation)

        # # Oblicz wartość sygnału sterującego i dodaj do listy
        # signal = self._regulator.pid_positional(self.deviations, self.params.t_p)
        ds = self._regulator.pid_incremental(self.deviations, self.params.t_p)
        if self.signals:
            signal = self.signals[-1] + ds
        else:
            signal = ds
        signal = max(signal, self.params.u_min)
        signal = min(signal, self.params.u_max)
        # signal = self._regulator.pid_positional(self.deviations, self.params.t_p)
        self.signals.append(signal)

        # # Przekonwertuj sygnał na nastawienie zaworu i dodaj do listy
        input_ = self._signal_to_input(signal)
        self.inputs.append(input_)

        self.energy_ins.append(self.inputs[-1] * self.params.t_p)
        self.energy_outs.append(self._sensor.get_energy_waste(self.readings[-1] - self.params.t_outside)
                                * self.params.t_p)

        # # Odczytaj aktualną temperaturę
        reading = self._sensor.read(prev_val=self.readings[-1], q_d=input_, t_p=self.params.t_p)
        self.readings.append(reading)

    def simulate(self):
        """Wykonuje symulację"""
        step_count = self.params.t_sim / self.params.t_p

        self.readings = [self.params.val_p]
        self.deviations = [self.params.val_ust - self.params.val_p]
        self.signals = []
        self.inputs = []
        self.energy_ins = [0]
        self.energy_ins_sums = [0]
        self.energy_outs = [0]
        self.energy_outs_sums = [0]
        for n in range(0, int(step_count)):
            self.make_step()

        self.count_sums(self.energy_ins, self.energy_ins_sums)
        self.count_sums(self.energy_outs, self.energy_outs_sums)

    def count_sums(self, array, array_sums):
        for i in range(1, len(array) - 1):
            if i < self.params.sum_length:
                array_sums.append(array_sums[i - 1] + array[i])
            else:
                array_sums.append(sum(array[i - self.params.sum_length + 1:i - 1]))

    def _signal_to_input(self, signal: float) -> float:
        """
        Zamienia sygnał otrzymany przez regurator na odpowiedni dopływ do systemu
        :param signal: Sygnał napięciowy otrzymany z regulatora
        :return: dopływ do systemu odpowiadający sygnałowi
        """
        # wspolczynnik kierunkowy
        u_range = self.params.u_max - self.params.u_min
        if u_range == 0:
            return 0
        a = (self.params.qd_max - self.params.qd_min) / u_range
        # wyraz wolny
        b = self.params.qd_min - a * self.params.u_min

        return a * signal + b
        # return self.efficiency * self._qd_max * signal

    def get_simulation_result(self):
        balance = []
        for i in range(0, len(self.energy_ins_sums)-1):
            balance.append(self.energy_ins_sums[i] - self.energy_outs_sums[i])

        dc = {
            'Krok': arange(0, self.params.t_sim, self.params.t_p),
            'Temperatura': self.readings[self.params.sum_length:-1],
            'Sygnaly': self.inputs[self.params.sum_length:],
            'Uchyby': self.deviations[self.params.sum_length:-1],
            'Dostarczane': self.energy_ins_sums[self.params.sum_length:],
            'Straty': self.energy_outs_sums[self.params.sum_length:],
            'Balans': balance[self.params.sum_length-1:]
        }
        diff = len(dc['Krok']) - len(dc['Temperatura'])
        if diff > 0:
            dc['Krok'] = dc['Krok'][:-diff]
        return pd.DataFrame(dc)

    def update_param(self, name, value):
        """
        Dynamicznie aktualizuje wartość parametru
        :param name: nazwa parametru
        :param value: nowa wartość
        """
        setattr(self.params, name, value)
        setattr(self._sensor.params, name, value)
        setattr(self._regulator.params, name, value)
        self.params.update_complex_params()
        self._sensor.params.update_complex_params()
        self._regulator.params.update_complex_params()

    def update_params(self, params: Parameter):
        """
        Aktualizuje parametry na posdtawie obiektu
        :param params: obiekt parametrów
        """
        params.update_complex_params()
        self.params = params
        self._sensor.params = params
        self._regulator.params = params
