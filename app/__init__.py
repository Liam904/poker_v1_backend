from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Load configurations from environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///game.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret")

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)  # You can specify origins if needed

    # Register blueprints
    from .views import views
    from .auth_routes import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app
