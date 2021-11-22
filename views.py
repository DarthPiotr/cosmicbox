from flask import Blueprint, render_template
from controller import Controller

from bokeh.embed import components
from bokeh.plotting import Figure
from bokeh.resources import INLINE

# configure blueprint

views = Blueprint('', __name__)


@views.route('/')
def index():
    """Home"""
    return render_template("index.html")


# Test
@views.route('/bokeh')
def bokeh():
    # https://github.com/saltastro/flask-start-setup/blob/master/docs/bokeh.md
    # https://docs.bokeh.org/en/latest/docs/user_guide/embed.html
    p = Figure(title='Sterowanie PID')

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    c = Controller()
    c.simulate()

    x = range(0, len(c.readings)-1)  # np.linspace(-10, 10, 200)
    y = c.readings[:-1]  # np.sin(x)

    p.line(x=x, y=y)

    script, div = components(p)

    return render_template('bokeh_test.html',
                           script=script, div=div,
                           js_resources=js_resources,
                           css_resources=css_resources)
