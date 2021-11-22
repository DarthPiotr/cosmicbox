from regulator import Regulator
from sensor import Sensor


class Controller:
    """Kontroler odpowiadający za współpracę aparatury pomiarowej i regulatora"""
    # TODO: zrobić wielkie sprzątanie

    # Regulator
    _regulator: Regulator
    """Regulator użyty do sterowania"""
    _u_min: float = 0.0
    """Minimalny sygnał reguratora"""
    _u_max: float = 10.0
    """Maksymalny sygnał reguratora"""

    # Sensor
    _sensor: Sensor
    """Czujnik wykonujący pomiary"""
    _val_min: float = 0
    """Minimalna wartość pomiaru"""
    _val_max: float = 10
    """Maksymalna wartość pomiaru"""

    # Pomieszczenie
    _qd_min: float = 0.0
    """Minimalne otwarcie zaworu (moc grzejnika)"""
    _qd_max: float = 0.05
    """Maksymalne otwarcie zaworu (moc grzejnika)"""


    # TODO: porządnie zaimplementować resztę pól - razem z implementacją pomieszczenia
    # - Symulacja
    h_p = 0.0  # [m]    - początkowa wysokość cieczy w zbiorniku
    h_ust = 1.5  # [m] - docelowa wysokość cieczy
    t_p = 0.1  # [s] - okres próbkowania
    t_sim = 1800  # [s] - czas symulacji
    readings = [h_p]  # odczyty; ustawienie wartości początkowej
    signals = []  # sygnały sterujące
    deviations = [h_ust - h_p]  # uchyby; ustawienie wartości początkowej
    inputs = []  # lista dopływów
    read_count = t_sim / t_p  # Wyliczenie ilośc iteracji

    def __init__(self):
        self._regulator = Regulator(u_min=self._u_min, u_max=self._u_max)
        self._sensor = Sensor(val_min=self._val_min, val_max=self._val_max)

    def make_step(self):
        """Wykonuje jeden krok symulacji"""
        # Oblicz uchyb i dodaj do listy
        deviation = self.h_ust - self.readings[-1]
        self.deviations.append(deviation)

        # # Oblicz wartość sygnału sterującego i dodaj do listy
        signal = self._regulator.pid_positional(self.deviations, self.t_p)
        self.signals.append(signal)

        # # Przekonwertuj sygnał na nastawienie zaworu i dodaj do listy
        input_ = self._signal_to_heat(signal)
        self.inputs.append(input_)

        # # Odczytaj aktualny poziom
        reading = self._sensor.read(prev_val=self.readings[-1], q_d=input_, t_p=self.t_p)
        self.readings.append(reading)

    def simulate(self):
        """Wykonuje symulację"""
        for n in range(0, int(self.read_count + 1)):
            self.make_step()

    def _signal_to_heat(self, signal: float) -> float:
        """Zamienia sygnał otrzymany przez regurator na odpowiedni dopływ do systemu"""
        a = (self._qd_max - self._qd_min) / (self._u_max - self._u_min)  # wspolczynnik kierunkowy
        b = self._qd_min - a * self._u_min               # wyraz wolny
        return a * signal + b


