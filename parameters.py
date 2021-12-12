class Parameter:
    """Zbiór wszystkich parametrów"""

    # Pomieszczenie
    val_p: float = 17.0
    """Początkowa wartość regulowanego parametru - temperatury"""
    val_ust: float = 21.0
    # 1.5
    """Docelowa wartość regulowanego parametru - temperatury"""

    qd_min: float = 0.0
    # _qd_min
    """Minimalne otwarcie zaworu (moc grzejnika)"""
    qd_max: float = 1000.0
    # _qd_max = 0.05
    """Maksymalne otwarcie zaworu (moc grzejnika)"""

    length = 5
    width = 5
    height = 3
    """wielkości powieszczenia [m]"""
    c = 1005 / 273.15
    """ciepło włąściwe powietrza [J / kg*K] -> st.C"""
    d = 1.2
    """gęstość powietrza w 20 st.C na poziomie morza [kg / m³]"""

    u1: float = 10 / 237.15
    # 1 - 0.2
    """współczynnik przenikania ciepła przez ściany [W/(m2*K)] -> st.C - na razie podany maxymalny"""
    u2: float = 20 / 273.15  # 0.9 / 273.15
    """współczynnik przenikania ciepła przez okno [W/(m2*K)] -> st.C - na razie podany maxymalny"""
    num_window = 1
    t_outside = 0
    """temp parametry"""
    open_wind = 0.2
    """współczynnik otwarcia okna"""
    s2: float = 1.6 * 0.5
    """powierzchnia okna (wymiany ciepła) [m2]"""
    s1: float = (2 * height * length + 2 * width * height) - (num_window * s2)
    """powierzchnia ściany (wymiany ciepła) [m2]"""
    efficiency = 0.8
    """sprawność urządzenia w przedziale (0; 1)"""

    # Symulacja
    t_p: float = 0.01
    """Okres próbkowania [s]"""
    t_sim: float = 100
    """Czas symulacji [s]"""

    # Regulator
    u_max: float = 10
    """Maksymalne napięcie wyjściowe"""
    u_min: float = 0
    """Minimalne napięcie wyjściowe"""
    k_p: float = 0.015
    """Wzmocnienie regulatora"""
    t_i: float = 0.05  # 0.05
    """Czas zdwojenia"""
    t_d: float = 0.25
    """Czas wyprzedzenia"""

    # Sensor
    val_min: float = -20
    """Minimalna wartość pomiaru"""
    val_max: float = 50
    """Maksymalna wartość pomiaru"""

    def get_parameters_dictionary(self):
        return {
            "Pokój": {
                # "<nazwa parametru [jednostka]>: [<wartość początkowa>, <min>, <max>, <krok>, <nazwa atrybutu>]
                "Temperatura początkowa [℃]":   [self.val_p, 0, 35, 0.1, "val_p"],
                "Temperatura docelowa [℃]":     [self.val_ust, 0, 35, 0.1, "val_ust"]
            },
            # "Sensor": {
            #
            # },
            # "Regulator": {
            #
            # },
            "Symulacja": {
                "Okres próbkowania [s]": [self.t_p, 0.005, 1, 0.005, "t_p"],
                "Czas symulacji [s]":    [self.t_sim, 10, 100, 10, "t_sim"]
            }
        }




