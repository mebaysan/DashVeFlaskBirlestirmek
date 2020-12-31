from flask import Flask
from myconfig import Config
from flaskapp.dashboard.apps.tips_dash.app import add_dash as add_tips_dash

def init_flask_app():
    core_app = Flask(__name__, instance_relative_config=False)
    core_app.config.from_object(Config)
    with core_app.app_context():
        from flaskapp import app
        core_app = add_tips_dash(core_app)
    return core_app
    