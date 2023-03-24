from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .blog import blog

load_dotenv()
db = SQLAlchemy()

