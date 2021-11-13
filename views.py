from flask import Blueprint, render_template

# configure blueprint
views = Blueprint('', __name__)


@views.route('/')
def index():
    """Home"""
    return render_template("page_template.html")
