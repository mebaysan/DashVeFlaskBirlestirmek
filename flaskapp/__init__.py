"""Bu dosya altında Flask uygulaması oluşturulur ve gerekli bileşenler import edilir """

from flask import Flask
from myconfig import Config
from flaskapp.db import db
from flaskapp.login import login
from flaskapp.dashboard.apps.tips_dash.app import add_dash as add_tips_dash
def init_flask_app():
    core_app = Flask(__name__, instance_relative_config=False)
    core_app.config.from_object(Config)
    db.init_app(core_app)
    login.init_app(core_app)
    with core_app.app_context():
        from flaskapp import app,context_processors,template_filters
        core_app = add_tips_dash(core_app)
    return core_app