from flask import Blueprint, render_template


from bokeh.embed import components, server_document
from bokeh.plotting import Figure
from bokeh.resources import INLINE
from tornado.ioloop import IOLoop

from controller import Controller
# configure blueprint

views = Blueprint('', __name__)


@views.route('/')
def index():
    """Home"""
    return render_template("index.html")

@views.route('/opinie')
def opinie():
    return render_template("opinions.html")

# Test
@views.route('/bokeh')
def bokeh():
    # https://github.com/saltastro/flask-start-setup/blob/master/docs/bokeh.md
    # https://docs.bokeh.org/en/latest/docs/user_guide/embed.html

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script = server_document('http://localhost:5006/bkapp')  # , div = components(p)

    return render_template('bokeh_test.html',
                           script=script,
                           js_resources=js_resources,
                           css_resources=css_resources)
