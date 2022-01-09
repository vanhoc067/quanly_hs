from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
login = LoginManager(app=app)
app.secret_key = '%$#%$^*&^(*&*&%*756759745rftgf5%E%%4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Az2882000@localhost/quanlyhs?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

cloudinary.config(
    cloud_name = 'duxlhasjq',
    api_key = '648295815347731',
    api_secret = 'A-U7OpxN-2jn2ZwahuxvKure10E'
)

