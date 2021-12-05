from threading import Thread

from flask import Flask

from views import views
from bokeh_config import bk_worker

import test

# Ten plik jest tylko do konfiguracji

app = Flask(__name__, static_folder='static')
app.register_blueprint(views)

# Start bokeh
Thread(target=bk_worker).start()

test.run()



