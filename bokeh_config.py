from functools import partial

import pandas as pd
from bokeh.layouts import column, layout, row, grid
from bokeh.models import ColumnDataSource, Slider, LayoutDOM, Panel, Tabs
from bokeh.plotting import figure
from bokeh.server.server import Server
from flask import session, app
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

    controller = Controller()
    controller.simulate()
    cds = controller.get_simulation_result()

    plot = figure(y_axis_label='Poziom cieczy (m)',
                  x_axis_label='Krok symulacji',
                  # y_range=(controller.val_min, controller.val_max),
                  title="Przebieg sterowania")
    ys = [cds['Poziom'], cds['Sygnaly'], cds['Uchyby']]
    xs = [cds['Krok']] * 3
    # plot.line('Krok', 'Poziom', source=source)
    data_dict = {
        'xs': xs,
        'ys': ys,
        'labels': ['Poziom', 'Sygnaly', 'Uchyby'],
        'line_color': ['#ff0000', '#00ff00', '#0000ff']
    }
    source = ColumnDataSource(data=data_dict)

    plot.multi_line(xs='xs', ys='ys', line_color='line_color', legend='labels', source=source)

    panels = []
    for category, params in controller.params.get_parameters_dictionary().items():
        sliders = []
        for name, values in params.items():
            slider = Slider(
                title=name,
                value=values[0],
                start=values[1],
                end=values[2],
                step=values[3]
            )

            def callback(attr, old, new, attrname):
                controller.update_param(attrname, new)
                controller.simulate()
                cds_ = controller.get_simulation_result()
                ys_ = [cds_['Poziom'], cds_['Sygnaly'], cds_['Uchyby']]
                xs_ = [cds_['Krok']] * 3
                data = {
                    'xs': xs_,
                    'ys': ys_,
                    'labels': ['Poziom', 'Sygnaly', 'Uchyby'],
                    'line_color': ['#ff0000', '#00ff00', '#0000ff']
                }
                source.data = data

            slider.on_change('value_throttled', partial(callback, attrname=values[4]))
            sliders.append(slider)
        panels.append(Panel(child=column(sliders), title=category))
    tabs = Tabs(tabs=panels)

    doc_layout = grid([
        [row(tabs, plot)]
    ],
        sizing_mode='stretch_width')

    doc.add_root(doc_layout)
