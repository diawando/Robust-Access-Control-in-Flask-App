from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .blog import blog

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://os.getenv("DB_USER"):os.getenv("DB_PASSWORD")@localhost:5432/rbac_blog"
    db.init_app(app)
    
    create_database(app)
    
    app.register_blueprint(blog, url_prefix="")
    return app

def create_database(app):
     with app.app_context():
         db.create_all()
     print("Database created")