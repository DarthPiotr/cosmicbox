import pandas as pd
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from controller import Controller


def bkapp(doc):

    c = Controller()
    c.simulate()

    x = range(0, len(c.readings) - 1)
    y = c.readings[:-1]

    cds = pd.DataFrame({'Czas': x, 'Poziom': y})

    source = ColumnDataSource(data=cds)

    plot = figure(y_axis_label='Poziom cieczy (m)', y_range=(0, 2),
                  title="Przebieg sterowania")
    plot.line('Czas', 'Poziom', source=source)

    def callback(attr, old, new):
        if new == 1.5:
            data = cds
        else:
            c.val_ust = new
            c.simulate()
            x_ = range(0, len(c.readings) - 1)
            y_ = c.readings[:-1]
            data = pd.DataFrame({'Czas': x_, 'Poziom': y_})
        source.data = data

    slider = Slider(start=0, end=2, value=1.5, step=0.1, title="Poziom docelowy")
    slider.on_change('value_throttled', callback)

    doc.add_root(column(slider, plot))


def bk_worker():
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:5000"])
    server.start()
    server.io_loop.start()