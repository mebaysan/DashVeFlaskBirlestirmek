class Config:
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = 'development'
    SECRET_KEY = 'cvhuylfd123qxpmrdm47681hds12'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = "postgresql://youtube:123456@localhost/Dash-FlaskDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False