from math import sqrt


class Sensor:
    """Czujnik temperatury wykonujący pomiary"""

    _val_min: float = 0
    """Minimalna wartość pomiaru"""
    _val_max: float = 10
    """Maksymalna wartość pomiaru"""

    def __init__(self,
                 val_min: float = 0,
                 val_max: float = 10):
        """
        Konstruktor z domyślnymi wartościami parametrów
        :param val_min:
        :param val_max:
        """
        self._val_min = val_min
        self._val_max = val_max

    def read(self, prev_val: float, q_d: float, t_p: float) -> float:
        """
        Wykonuje odczyt na podstawie równania różnicowego
        :param prev_val: wartość poprzedniego odczytu
        :param q_d: wartość obecnego wpływu do układu (np. obecna przepustowość pompy, moc grzejnika)
        :param t_p: okres próbkowania symulacji
        :return: wartość nowego odczytu
        """
        # TODO: zaimplementować logikę dla pomieszczenia i temperatury
        # Chwilowo skopiowany kod zbiornika
        a = 1.5
        """Pole powierzchni dna zbiornika [m2] - przykład docstringa"""
        beta = 0.035
        """Wpółczynnik wypływu [m^(5/2)/s]"""

        reading = float(1 / a * (-beta * sqrt(prev_val) + q_d) * t_p + prev_val)

        if reading > self._val_max or reading < self._val_min:
            # print("[!] Wartość pomiaru przekracza ekstremum")
            reading = max(reading, self._val_min)
            reading = min(reading, self._val_max)
        return reading
