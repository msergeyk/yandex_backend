import warnings

from flask import Flask

from app.views import views

app = Flask(__name__)

app.register_blueprint(views)

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
