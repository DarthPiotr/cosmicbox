from parameters import Parameter


class Regulator:
    """Regulator PID"""

    params: Parameter
    """Aktualne wartości parametrów"""

    def __init__(self, params: Parameter):
        """
        Konstruktor z domyślnymi wartościami parametrów
        :param params: obiekt z parametrami
        """
        self.params = params

    def pid_positional(self, e_list: list, t_p: float):
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
        u = self.params.k_p * (e + ((t_p / self.params.t_i) * sigma_e) + ((self.params.t_d / t_p) * delta_e))
        # make sure output is in range
        u = max(min(u, self.params.u_max), self.params.u_min)

        return u

    def pid_incremental(self, current_e: float, previous_e: float, t_p: float):
        """
        Algorytm sterowania PID (przyrostowy)
        :param current_e: obecny uchyb
        :param previous_e: poprzedni uchyb
        :param t_p: okres próbkowania
        :return: zmiana sygnału napięciowego
        """

        delta_e = current_e - previous_e

        # PID
        u = self.params.k_p * (delta_e + ((t_p / self.params.t_i) * current_e) +
                               ((self.params.t_d / t_p) * delta_e * delta_e))

        return u
