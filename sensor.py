from parameters import Parameter


class Sensor:
    """Czujnik temperatury wykonujący pomiary"""

    params: Parameter
    """Aktualne wartości parametrów"""

    # _val_min: float = 0
    # """Minimalna wartość pomiaru"""
    # _val_max: float = 10
    # """Maksymalna wartość pomiaru"""

    def __init__(self,
                 # val_min: float = 0,
                 # val_max: float = 10
                 params: Parameter):
        """
        Konstruktor z domyślnymi wartościami parametrów

        """
        self.params = params
        # :param val_min:
        # :param val_max:
        # self._val_min = val_min
        # self._val_max = val_max

    def read(self, prev_val: float, q_d: float, t_p: float) -> float:
        """
        Wykonuje odczyt na podstawie równania różnicowego
        :param prev_val: wartość poprzedniego odczytu
        :param q_d: wartość obecnego wpływu do układu (cipło dostarczane)
        :param t_p: okres próbkowania symulacji
        :return: wartość nowego odczytu
        """
        volume = self.params.length * self.params.width * self.params.height

        # q_s = 1000*wasted

        # # Straty ciepła
        wasted = float(
            ((self.params.u1 * self.params.s1) + (self.params.open_wind * self.params.u2 * self.params.s2)) * (
                    prev_val - self.params.t_outside))

        reading = float(((q_d - wasted) / (self.params.c * self.params.d * volume)) * t_p + prev_val)
        if reading > self.params.val_max or reading < self.params.val_min:
            # print("[!] Wartość pomiaru przekracza ekstremum")
            reading = max(reading, self.params.val_min)
            reading = min(reading, self.params.val_max)
        return reading
