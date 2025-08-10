# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()  # reads .env in project root if present

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///dental.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET", "jwt-secret")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # blueprints
    from .auth import auth_bp
    from .clinics import clinic_bp
    from .api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(clinic_bp, url_prefix="/clinic")
    app.register_blueprint(api_bp, url_prefix="/api")

    # Add a root route
    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

    return app
