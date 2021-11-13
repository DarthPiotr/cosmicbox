from math import sqrt


class Sensor:
    """Czujnik temperatury wykonujący pomiary"""

    def read(self, prev_val: float, q_d: float, t_p: float) -> float:
        # TODO: zaimplementować logikę dla pomieszczenia i temperatury
        # Chwilowo skopiowany kod zbiornika
        # - Zbiornik
        A = 1.5  # [m2] - pole powierzchni przekroju (dna zbiornika)
        beta = 0.035  # [m^(5/2)/s] - wpółczynnik wypływu
        h_min = 0.0  # [m]    - minimalna wysokość cieczy
        h_max = 10.0  # [m]    - maksymalna wysokość cieczy

        h = prev_val  # ostatni odczyt
        reading = float(1 / A * (-beta * sqrt(h) + q_d) * t_p + h)
        if reading > h_max or reading < h_min:
            # print("[!] Wartość pomiaru przekracza ekstremum")
            reading = max(reading, h_min)
            reading = min(reading, h_max)
        return reading
