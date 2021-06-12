from flask import Flask
# from flask_script import Manager
# from flask_manager import Migrate, MigrateCommand
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class Config(object):
    DEBUG = True


app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def index():
    return "Hello Flask"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
