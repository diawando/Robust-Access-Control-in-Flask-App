from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .blog import blog
from flask_login import LoginManager
from .auth import auth


load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_PATH")
    db.init_app(app)
    
    create_database(app)
    
    login_manager = LoginManager() # handless session for users
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        with app.app_context():
            return User.query.get(int(id))
    
    app.register_blueprint(blog, url_prefix="")
    app.register_blueprint(auth, url_prefix="/auth")
    return app

def create_database(app):
     with app.app_context():
         db.create_all()
     print("Database created")