from flask import render_template
from flask import current_app as app
from flaskapp.dashboard.urls import URL_PATHS


@app.route('/')
def index():
    return render_template('index.jinja2', title='Anasayfa')


@app.route('/dashboard/<string:dash_url>')
def get_dash(dash_url):
    CONFIG = next(filter(lambda x: x['APP_URL'] == dash_url, URL_PATHS), None)
    if not CONFIG:
        return "404"
    return render_template('dashboard_basic.jinja2', dash_url=CONFIG['BASE_URL'],
                           dash_min_height=CONFIG['MIN_HEIGHT'], title=CONFIG['APP_NAME'])
