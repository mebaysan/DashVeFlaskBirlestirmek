from flask import current_app as app
from flask_login import current_user
from flaskapp.models.user import RoleModel

@app.template_filter()
def is_my_role(role_url):
    role = RoleModel.find_by_name(role_url)
    return current_user.is_my_role(role)