import re
from decimal import Context
from functools import partial

from os import listdir
from bokeh.layouts import column, row, grid
from bokeh.models import ColumnDataSource, Slider, Panel, Tabs, Range1d, LinearAxis, Legend, LegendItem, RangeSlider, \
    Button
from bokeh.plotting import figure
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from controller import Controller
from parameters import Parameter

bokeh_port = 5001


def bk_worker():
    """Inicjalizacja serwera Bokeh"""
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:5000"], port=bokeh_port)
    server.start()
    server.io_loop.start()


def bkapp(doc):
    """Zwraca wykres i slidery"""

    # Stwórz kontroler i przeprowadź symulację
    controller = Controller()
    controller.simulate()
    cds = controller.get_simulation_result()

    # Przygotuj wykres i lewą oś (temperatury)
    plot = figure(y_axis_label='Temperatura pomieszczenia [℃]',
                  x_axis_label='Czas symulacji [s]',
                  y_range=Range1d(start=-1,
                                  end=controller.params.val_max * 1.1),
                  title="Przebieg sterowania", height=500, sizing_mode="stretch_width")
    # Dodaj prawą oś (mocy grzejnika)
    plot.extra_y_ranges = {"y_inputs": Range1d(
        start=controller.params.qd_min - 10,
        end=controller.params.qd_max * 1.1  # ,
        # bounds=(-controller.params.qd_max * 1.1, controller.params.qd_max * 1.5)
    )}
    plot.add_layout(LinearAxis(y_range_name='y_inputs', axis_label='Moc grzejnika [W]'), 'right')

    # Przygotuj dane do wyświetlenia
    data_dict_temp, data_dict_deviation, data_dict_input = dict_from_cds(cds)
    source_temp = ColumnDataSource(data=data_dict_temp)
    source_deviation = ColumnDataSource(data=data_dict_deviation)
    source_input = ColumnDataSource(data=data_dict_input)

    # Narysuj linie na wykresie
    lines_temp = plot.multi_line(xs='xs', ys='ys', line_color='line_color', source=source_temp)
    lines_deviation = plot.multi_line(xs='xs', ys='ys', line_color='line_color', source=source_deviation)
    lines_input = plot.multi_line(xs='xs', ys='ys', line_color='line_color', source=source_input,
                                  y_range_name='y_inputs')

    lines_deviation.visible = False

    # przygotuj legendę
    legend = Legend(items=[
        LegendItem(label='Poziom', renderers=[lines_temp], index=0),
        LegendItem(label='Uchyby', renderers=[lines_deviation], index=0),
        LegendItem(label='Moc grzejnika', renderers=[lines_input], index=0)
    ])
    plot.add_layout(legend)
    plot.legend.click_policy = 'hide'

    # Presety
    buttons = []
    for file in listdir("./presets"):
        if file.endswith(".json"):
            button = Button(label=file[:-5])
            buttons.append(button)

            def callback_button(event, filename):
                # Zaktualizuj parametr i przeprowadź nową symulację
                controller.update_params(Parameter.from_json(filename))
                controller.simulate()

                # Zaktualizuj źródła danych wykresu
                cds_ = controller.get_simulation_result()
                data_temp_, data_deviation_, data_input_ = dict_from_cds(cds_)
                source_temp.data = data_temp_
                source_deviation.data = data_deviation_
                source_input.data = data_input_

                # Dodaj callback do zdarzenia wybrania nowej wartości suwakiem

            button.on_click(partial(callback_button, filename="./presets/"+file))

    presets = column(children=buttons)

    # Przygotuj parametry na stronie na podstawie słownika
    parameters_dict = controller.params.get_parameters_dictionary()
    panels = []
    # Dla każdej kategorii
    for category, params in parameters_dict.items():
        sliders = []
        # Wczytaj każdy parametr
        for name, values in params.items():
            # Stwórz slider
            if type(values[0]) is tuple:
                slider = RangeSlider(
                    title=name,
                    value=values[0],
                    start=values[1],
                    end=values[2],
                    step=values[3],
                    format=get_format_from_number(values[3]),
                    name=values[4]
                )
            else:
                slider = Slider(
                    title=name,
                    value=values[0],
                    start=values[1],
                    end=values[2],
                    step=values[3],
                    format=get_format_from_number(values[3])
                )

            # Zdefinuj funkcję używaną do zmiany wartości suwakiem
            # noinspection PyUnusedLocal
            def callback_slider(attr, old, new, attrname):
                # Zaktualizuj parametr i przeprowadź nową symulację
                if type(new) is tuple:  # dla RangeSliderów
                    for i, attr_name in enumerate(attrname.split(",")):
                        controller.update_param(attr_name, new[i])
                else:
                    controller.update_param(attrname, new)
                controller.simulate()

                # Zaktualizuj źródła danych wykresu
                cds_ = controller.get_simulation_result()
                data_temp_, data_deviation_, data_input_ = dict_from_cds(cds_)
                source_temp.data = data_temp_
                source_deviation.data = data_deviation_
                source_input.data = data_input_

            # Dodaj callback do zdarzenia wybrania nowej wartości suwakiem
            slider.on_change('value_throttled', partial(callback_slider, attrname=values[4]))

            # Dodaj nowy suwak do obecnej kategorii
            sliders.append(slider)

        # Dodaj wszystkie suwaki z kategorii do nowej zakładki
        panels.append(Panel(child=column(sliders), title=category))

    # Stwórz widok z wszystkimi zakładkami
    tabs = Tabs(tabs=panels)

    # Wygeneruj widok z parametrami i wykresem
    doc_layout = grid([
        [row(column(presets, tabs), plot)]
    ],
        sizing_mode='stretch_width')

    # Zwróć widok na stronę
    doc.add_root(doc_layout)


def get_format_from_number(step: float):
    if step >= 1:
        return '0'
    res = re.sub('[1-9]', '0', float_to_str(step))
    return res


ctx = Context()
ctx.prec = 20


def float_to_str(a: float):
    d1 = ctx.create_decimal(repr(a))
    return format(d1, 'f')


def dict_from_cds(cds):
    """
    Tworzy słowniki do wyświetlania wykresów
    :param cds: dane z symulacji
    :return: słowniki z danymi temperatury oraz mocy grzejnika
    """
    data_dict_temp = {
        'xs': [cds['Krok']],
        'ys': [cds['Poziom']],
        'line_color': ['#ff0000']
    }
    data_dict_deviation = {
        'xs': [cds['Krok']],
        'ys': [cds['Uchyby']],
        'line_color': ['#0000ff']
    }
    data_dict_input = {
        'xs': [cds['Krok']],
        'ys': [cds['Sygnaly']],
        'line_color': ['#00ff00']
    }
    return data_dict_temp, data_dict_deviation, data_dict_input
