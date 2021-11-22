from regulator import Regulator
from sensor import Sensor


class Controller:
    """Kontroler odpowiadający za współpracę aparatury pomiarowej i regulatora"""

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
    val_p: float = 0
    """Początkowa wartość regulowanego parametru"""
    val_ust: float = 1.5
    """Docelowa wartość regulowanego parametru"""

    _qd_min: float = 0.0
    """Minimalne otwarcie zaworu (moc grzejnika)"""
    _qd_max: float = 0.05
    """Maksymalne otwarcie zaworu (moc grzejnika)"""

    # Symulacja
    t_p: float = 0.1
    """Okres próbkowania [s]"""
    t_sim: float = 1800
    """Czas symulacji [s]"""
    readings: list = []
    """Lista odczytów"""
    signals: list = []
    """Lista wygnałów sterujących"""
    deviations: list = []
    """Lista uchybów"""
    inputs: list = []
    """Lista wartości 'wpływów' do układu"""

    def __init__(self):
        self._regulator = Regulator(u_min=self._u_min, u_max=self._u_max)
        self._sensor = Sensor(val_min=self._val_min, val_max=self._val_max)
        self.readings = [self.val_p]
        self.deviations = [self.val_ust - self.val_p]

    def make_step(self):
        """Wykonuje jeden krok symulacji (pozycyjnie)"""
        # Oblicz uchyb i dodaj do listy
        deviation = self.val_ust - self.readings[-1]
        self.deviations.append(deviation)

        # # Oblicz wartość sygnału sterującego i dodaj do listy
        signal = self._regulator.pid_positional(self.deviations, self.t_p)
        self.signals.append(signal)

        # # Przekonwertuj sygnał na nastawienie zaworu i dodaj do listy
        input_ = self._signal_to_input(signal)
        self.inputs.append(input_)

        # # Odczytaj aktualny poziom
        reading = self._sensor.read(prev_val=self.readings[-1], q_d=input_, t_p=self.t_p)
        self.readings.append(reading)

    def simulate(self):
        """Wykonuje symulację"""
        step_count = self.t_sim / self.t_p
        for n in range(0, int(step_count + 1)):
            self.make_step()

    def _signal_to_input(self, signal: float) -> float:
        """
        Zamienia sygnał otrzymany przez regurator na odpowiedni dopływ do systemu
        :param signal: Sygnał napięciowy otrzymany z regulatora
        :return: dopływ do systemu odpowiadający sygnałowi
        """
        a = (self._qd_max - self._qd_min) / (self._u_max - self._u_min)  # wspolczynnik kierunkowy
        b = self._qd_min - a * self._u_min               # wyraz wolny
        return a * signal + b


