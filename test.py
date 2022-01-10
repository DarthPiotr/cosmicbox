from controller import Controller


def run():
    """Wykonuje kod w ramach testów"""
    controller = Controller()
    controller.update_param("u_min", -3)
    controller.update_param("u_max", -1)
    controller.update_param("qd_min", 1)
    controller.update_param("qd_max", 3)
    # noinspection PyProtectedMember
    assert controller._signal_to_input(-2) == 2.0



