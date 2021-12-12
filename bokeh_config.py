from functools import partial
from bokeh.layouts import column, row, grid
from bokeh.models import ColumnDataSource, Slider, Panel, Tabs, Range1d, LinearAxis, Legend, LegendItem
from bokeh.plotting import figure
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from controller import Controller

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

    plot = figure(y_axis_label='Temperatura pomieszczenia [℃]',
                  x_axis_label='Krok symulacji',
                  y_range=(-controller.params.val_max * 1.1, controller.params.val_max * 1.1),
                  title="Przebieg sterowania")
    plot.extra_y_ranges = {"y_inputs": Range1d(start=controller.params.qd_min - 10,
                                               end=controller.params.qd_max * 1.1)}
    plot.add_layout(LinearAxis(y_range_name='y_inputs', axis_label='Moc grzejnika [W]'), 'right')

    data_dict_temp, data_dict_input = dict_from_cds(cds)
    source_temp = ColumnDataSource(data=data_dict_temp)
    source_input = ColumnDataSource(data=data_dict_input)

    # plot.multi_line(xs='xs', ys='ys', line_color='line_color', legend='labels', source=source)
    lines_temp = plot.multi_line(xs='xs', ys='ys', line_color='line_color', source=source_temp)
    # plot.line(x=xs2, y=ys2, line_color='#00ff00', y_range_name='y_inputs', legend='Sygnały')
    lines_input = plot.multi_line(xs='xs', ys='ys', line_color='line_color', source=source_input,
                                  y_range_name='y_inputs')
    legend = Legend(items=[
        LegendItem(label='Poziom', renderers=[lines_temp], index=0),
        LegendItem(label='Uchyby', renderers=[lines_temp], index=1),
        LegendItem(label='Moc grzejnika', renderers=[lines_input], index=0)
    ])
    plot.add_layout(legend)

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
                data_temp_, data_input_ = dict_from_cds(cds_)

                source_temp.data = data_temp_
                source_input.data = data_input_

            slider.on_change('value_throttled', partial(callback, attrname=values[4]))
            sliders.append(slider)
        panels.append(Panel(child=column(sliders), title=category))
    tabs = Tabs(tabs=panels)

    doc_layout = grid([
        [row(tabs, plot)]
    ],
        sizing_mode='stretch_width')

    doc.add_root(doc_layout)


def dict_from_cds(cds):
    # plot.line('Krok', 'Poziom', source=source)
    data_dict_temp = {
        'xs': [cds['Krok']] * 2,
        'ys': [cds['Poziom'], cds['Uchyby']],
        'line_color': ['#ff0000', '#0000ff']
    }
    data_dict_input = {
        'xs': [cds['Krok']],
        'ys': [cds['Sygnaly']],
        'line_color': ['#00ff00']
    }
    return data_dict_temp, data_dict_input
