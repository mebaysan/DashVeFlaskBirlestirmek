from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flaskapp.models.user import UserModel, RoleModel
from flaskapp.db import db

app = Blueprint('admin', __name__)


@app.route('/')
@login_required
def index():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    users = UserModel.get_all()
    roles = RoleModel.get_all()
    return render_template('admin/index.jinja2', users=users, roles=roles)


@app.route('/user/add', methods=['POST'])
@login_required
def user_add():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = True if request.form.get('is_admin') == 'True' else False
    if UserModel.find_by_username(username):
        flash(f'{username} Zaten mevcut! Başka bir kullanıcı adı deneyin', 'warning')
        return redirect(url_for('admin.index'))
    new_user = UserModel(username=username, password=password, is_admin=is_admin)
    new_user.set_password(password)
    new_user.save_to_db()
    flash(f'{username} Kullanıcısı başarıyla eklendi!', 'success')
    return redirect(url_for('admin.index'))


@app.route('/user/delete/<int:id>', methods=['POST'])
@login_required
def user_delete(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    user = UserModel.find_by_id(id)
    user.delete_from_db()
    flash(f'{user.username} Kullanıcısı başarıyla silindi!', 'success')
    return redirect(url_for('admin.index'))


@app.route('/user/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def user_detail(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    user = UserModel.find_by_id(id)
    roles = RoleModel.get_all()
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.is_admin = True if request.form.get('is_admin') == 'True' else False
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        user.roles.clear()
        roles = request.form.getlist('roles')
        for role in roles:
            user.roles.append(RoleModel.find_by_id(role))
        user.save_to_db()
        flash(f'{user.username} Başarıyla güncellendi!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/user_detail.jinja2', user=user, roles=roles)


@app.route('/role/add', methods=['POST'])
@login_required
def role_add():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    role_name = request.form.get('role_name')
    if RoleModel.find_by_name(role_name):
        flash(f'{role_name} Zaten mevcut! Başka bir rol adı deneyin', 'warning')
        return redirect(url_for('admin.index'))
    new_role = RoleModel(role_name)
    new_role.save_to_db()
    flash(f'{new_role.name} Rolü başarıyla eklendi!', 'success')
    return redirect(url_for('admin.index'))


@app.route('/role/delete/<int:id>', methods=['POST'])
@login_required
def role_delete(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    role = RoleModel.find_by_id(id)
    role.delete_from_db()
    flash(f'{role.name} Rolü başarıyla silindi!', 'success')
    return redirect(url_for('admin.index'))
