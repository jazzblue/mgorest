from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config.from_object('mgorest.configmodule.DevelopmentConfig')  # Import configuration

db.init_app(app)

from v1_0.routes import api as api_v1_0

# Default version (currently points to v1_0)
app.register_blueprint(api_v1_0, url_prefix='')

# Versions
app.register_blueprint(api_v1_0, url_prefix='/v1_0')
