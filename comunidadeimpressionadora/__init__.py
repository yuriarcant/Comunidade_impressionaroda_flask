from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
import os



app.config['SECRET_KEY']= 'c8b69b71e54ec4777fc66d232935fcbe'

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('BANCO_DADOS_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view= 'login'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes
