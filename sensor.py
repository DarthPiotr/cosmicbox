from parameters import Parameter


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

    def read(self, prev_val: float, q_d: float, q_s: float, t_p: float) -> float:
        """
        Wykonuje odczyt na podstawie równania różnicowego
        :param prev_val: wartość poprzedniego odczytu
        :param q_d: wartość obecnego wpływu do układu (cipło dostarczane)
        :param q_s: wartość obecnego wypływu z układu (straty cipła)
        :param t_p: okres próbkowania symulacji
        :return: wartość nowego odczytu
        """
        volume = Parameter.length * Parameter.width * Parameter.height

        q_s = 1000*q_s

        # # Straty ciepła
        wasted = float(
            ((Parameter.u1 * Parameter.s1) + (Parameter.open_wind * Parameter.u2 * Parameter.s2)) * (prev_val - Parameter.t_outside))

        reading = float(((q_d - q_s) / (c * d * volume)) * t_p + prev_val)
        if reading > self._val_max or reading < self._val_min:
            # print("[!] Wartość pomiaru przekracza ekstremum")
            reading = max(reading, self._val_min)
            reading = min(reading, self._val_max)
        return reading
