from flask import Blueprint, render_template, request

from bokeh.embed import server_document
from bokeh.resources import INLINE
from bokeh_config import bokeh_port

# configure blueprint

views = Blueprint('', __name__)


@views.route('/')
def index():
    """Home"""
    return render_template("index.html")


@views.route('/opinie')
def opinie():
    return render_template("opinions.html")


@views.route('/projekt')
def projekt():
    return render_template("project.html")


@views.route('/cennik')
def cennik():
    return render_template("prices.html")


# Test
@views.route('/bokeh')
def bokeh():
    # https://github.com/saltastro/flask-start-setup/blob/master/docs/bokeh.md
    # https://docs.bokeh.org/en/latest/docs/user_guide/embed.html

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script = server_document(f'http://localhost:{bokeh_port}/bkapp')

    return render_template('bokeh_test.html',
                           script=script,
                           js_resources=js_resources,
                           css_resources=css_resources)
