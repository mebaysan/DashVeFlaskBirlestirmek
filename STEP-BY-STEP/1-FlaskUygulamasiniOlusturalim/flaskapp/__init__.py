from flask import Flask
from myconfig import Config

def init_flask_app():
    core_app = Flask(__name__, instance_relative_config=False)
    core_app.config.from_object(Config)
    with core_app.app_context():
        from flaskapp import app
    return core_app
    