from flask import Flask
from views import views

# import test

# This file is for configuration only

app = Flask(__name__, static_folder='static')
app.register_blueprint(views)

# test.run()
