from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__, static_folder='static')


app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.init_app(app)
migrate.init_app(app)
cors.init_app(app)

from app import routes

# open shell and run python command:
#   from app import app, db
