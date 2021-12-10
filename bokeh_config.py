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

    def callback(attr, old, new):
        if new == 1.5:
            data = data_dict
        else:
            Parameter.val_ust = new
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

    sl_vasl_ust = Slider(start=controller.val_min,
                         end=controller.val_max,
                         value=Parameter.val_ust,
                         step=0.1,
                         title="Poziom docelowy")
    sl_vasl_ust.on_change('value_throttled', callback)
    # slider = [ sl_vasl_ust ]

    sl_test: LayoutDOM = Slider(start=0,
                     end=5,
                     value=2.5,
                     step=0.1,
                     title="Test")

    l1 = layout([[sl_vasl_ust]])
    l2 = layout(sl_test)
    t1 = Panel(child=l1, title="Tab 1")
    t2 = Panel(child=l2, title="Tab 2")
    tabs = Tabs(tabs=[t1, t2])

    doc_layout = grid([
        [row(tabs, plot)]
    ],
        sizing_mode='stretch_width')

    doc.add_root(doc_layout)


def bk_worker():
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:5000"], port=bokeh_port)
    server.start()
    server.io_loop.start()
