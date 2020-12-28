"""Bu dosya __init__.py içerisinde oluşturulmuş Flask uygulamasını serve eder"""

from flaskapp import init_flask_app

if __name__ == '__main__':
    app = init_flask_app()
    app.run()