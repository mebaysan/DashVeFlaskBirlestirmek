"""ana Flask uygulamamıza ait route'lar"""
from flask import render_template, redirect, url_for, request,flash
from flask import current_app as app
from flaskapp.dashboard.urls import URL_PATHS
from flaskapp.db import db
from flaskapp.models.user import UserModel
from flaskapp.login import login
from flask_login import current_user, login_required, login_user, logout_user
from flaskapp.admin.app import app as admin_bp

@app.before_first_request
def create_tables():
    db.create_all()


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@login.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.jinja2', title='Anasayfa')


@app.route('/dashboard/<string:dash_url>')
@login_required
def get_dash(dash_url):
    CONFIG = next(filter(lambda x: x['APP_URL'] == dash_url, URL_PATHS),None)
    if not CONFIG:
        flash('Aradığınız Dashboard bulunamadı', 'danger')
        return redirect(url_for('index'))
    role = RoleModel.find_by_name(dash_url)
    if current_user.is_my_role(role):
        return render_template('dashboards/dashboard_basic.jinja2', dash_url=CONFIG['BASE_URL'],
                               dash_min_height=CONFIG['MIN_HEIGHT'],
                               title=CONFIG['APP_NAME'])
    else:
        flash('Bu dashboardu görmek için yetkiye sahip değilsiniz', 'warning')
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.find_by_username(username)
        if user is None or not user.check_password(password):
            flash('Kullanıcı Adı veya Parola Hatalı!', 'danger')
            return render_template('login.jinja2', title='Giriş')
        login_user(user)
        flash('Başarılı bir şekilde giriş yapıldı', 'success')
        return redirect(url_for('index'))
    return render_template('login.jinja2', title='Giriş')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarılı bir şekilde çıkış yapıldı!', 'success')
    return redirect(url_for('index'))

app.register_blueprint(admin_bp, url_prefix='/admin')