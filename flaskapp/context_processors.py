"""Bu dosya context processorleri yazdığımız dosya"""

from flask import current_app as app
from flaskapp.dashboard.urls import URL_PATHS


@app.context_processor
def get_dashboards():
    return dict(get_dashboards=URL_PATHS)