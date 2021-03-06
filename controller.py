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
    """Aktualne wartości parametrów"""
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

        # # Odczytaj aktualny poziom
        reading = self._sensor.read(prev_val=self.readings[-1], q_d=input_, t_p=self.params.t_p)
        self.readings.append(reading)

    def simulate(self):
        """Wykonuje symulację"""
        step_count = self.params.t_sim / self.params.t_p
        self.readings = [self.params.val_p]
        self.deviations = [self.params.val_ust - self.params.val_p]
        self.signals = []
        self.inputs = []
        for n in range(0, int(step_count)):
            self.make_step()
        # print("Aktualny poziom: ", self.readings)
        # print("Uchyb: ", self.deviations)
        # print("Sygnał sterujący: ", self.signals)
        # print("Nastawienie zaworu: ", self.inputs)

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
        dc = {
            'Krok': arange(0, self.params.t_sim, self.params.t_p),
            'Temperatura': self.readings[:-1],
            'Sygnaly': self.inputs,
            'Uchyby': self.deviations[:-1]
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
