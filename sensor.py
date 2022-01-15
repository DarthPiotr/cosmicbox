from parameters import Parameter


class Sensor:
    """Czujnik temperatury wykonujący pomiary"""

    params: Parameter
    """Aktualne wartości parametrów"""

    def __init__(self, params: Parameter):
        """
        Konstruktor z domyślnymi wartościami parametrów
        """
        self.params = params

    def read(self, prev_val: float, q_d: float, t_p: float) -> float:
        """
        Wykonuje odczyt na podstawie równania różnicowego
        :param prev_val: wartość poprzedniego odczytu
        :param q_d: wartość obecnego wpływu do układu (cipło dostarczane)
        :param t_p: okres próbkowania symulacji
        :return: wartość nowego odczytu
        """
        volume = self.params.length * self.params.width * self.params.height
        t_outside = self.cap_temperature(self.params.t_outside)
        # # Straty ciepła
        wasted = float(
            ((self.params.u1 * self.params.s1)  # ściany
             + (self.params.num_window * self.params.open_wind * self.params.u2 * self.params.s2))  # okna
            * (prev_val - t_outside))

        reading = float(((q_d - wasted) / (self.params.c * self.params.d * volume)) * t_p + prev_val)

        return self.cap_temperature(reading)

    def cap_temperature(self, temperature):
        """
        Ogranicza temperaturę do wartości odczytywanych przez sensor
        :param temperature: temperatura wejściowa
        :return: Ograniczona temperatura
        """
        return max(self.params.val_min, min(self.params.val_max, temperature))
