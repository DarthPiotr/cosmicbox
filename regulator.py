class Regulator:
    """Regulator PID"""

    _u_max: float = 10
    """Maksymalne napięcie wyjściowe"""
    _u_min: float = 0
    """Minimalne napięcie wyjściowe"""
    _k_p: float = 0.015
    """Wzmocnienie wrgulatora"""
    _t_i: float = 0.05
    """czas zdwojenia"""
    _t_d: float = 0.25
    """czas wyprzedzenia"""

    def pid_positional(self, e_list: list, t_p: int):
        """
        Algorytm sterowania PID (pozycyjny)
        :param e_list: lista wszystkich uchybów
        :param t_p: okres próbkowania
        :return: sygnał napięciowy z zakresu <_u_min; _u_max>
        """
        e = e_list[-1]
        sigma_e = sum(e_list)
        delta_e = e_list[-2] - e_list[-1]

        # PID
        u = self._k_p * (e + ((t_p / self._t_i) * sigma_e) + ((self._t_d / t_p) * delta_e))
        # make sure output is in range
        u = max(min(u, self._u_max), self._u_min)

        return u

    def pid_incremental(self, current_e: float, previous_e: float, t_p: int):
        """
        Algorytm sterowania PID (przyrostowy)
        :param current_e: obecny uchyb
        :param previous_e: poprzedni uchyb
        :param t_p: okres próbkowania
        :return: zmiana sygnału napięciowego
        """

        delta_e = current_e - previous_e

        # PID
        u = self._k_p * (delta_e + ((t_p / self._t_i) * current_e) + ((self._t_d / t_p) * delta_e * delta_e))

        return u
