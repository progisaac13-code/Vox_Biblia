import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'MchaOpqQ12@1#ÇQ2Qxvsokq-1203331m'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/vox_biblia?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from app.routes import index

