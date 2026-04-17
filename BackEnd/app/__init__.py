# Connects to the database using the info in the .env file and initates different resources

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# load environment
load_dotenv()

assert(os.getenv('DB_USERNAME') and os.getenv('DB_PASSWORD') and os.getenv('DB_URL'))

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URL')}' # mysql+pymysql_driver/username:password@ip/db_name

    app.config['JWT_SECRET_KEY'] = '6M2nCYz7YshYcaRoF4_jXeLnR0aCz2NBJjR4xVRF0bA'  
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # token expiration.

    jwt = JWTManager(app)

    db.init_app(app)
    bcrypt.init_app(app)

    from app.models import User

    from app.views import views_bp
    app.register_blueprint(views_bp)

    return app