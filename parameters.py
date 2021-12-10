class Parameter:
    """Zbiór wszystkich parametrów"""

    # # Regulator
    # _regulator: Regulator
    # """Regulator użyty do sterowania"""
    # _u_min: float = -5.0
    # """Minimalny sygnał reguratora"""
    # _u_max: float = 35.0
    # """Maksymalny sygnał reguratora"""
    #
    # # Sensor
    # _sensor: Sensor
    # """Czujnik wykonujący pomiary"""
    # _val_min: float = 0.0
    # """Minimalna wartość pomiaru"""
    # _val_max: float = 35.0
    # # 2
    # """Maksymalna wartość pomiaru"""

    # Pomieszczenie
    val_p: float = 0.0
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

    # Symulacja
    t_p: float = 0.01
    """Okres próbkowania [s]"""
    t_sim: float = 18
    """Czas symulacji [s]"""

    length = 5
    width = 5
    height = 3
    """wielkości powieszczenia [m]"""
    c = 1005 / 273.15
    """ciepło włąściwe powietrza [J / kg*K] -> st.C"""
    d = 1.2
    """gęstość powietrza w 20 st.C na poziomie morza [kg / m³]"""

    u1: float = 2 / 237.15
    # 1 - 0.2
    """współczynnik przenikania ciepła przez ściany [W/(m2*K)] -> st.C - na razie podany maxymalny"""
    u2: float = 0.9 / 273.15
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




