from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
import os
import sqlalchemy



app.config['SECRET_KEY']= 'c8b69b71e54ec4777fc66d232935fcbe'

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI']= 'aqui ficaria  link para bancode dados online'
else:
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view= 'login'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table('usuario'):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('base de dados criadas con ssucesso')
else:
    print('base de dados ja existente')

from comunidadeimpressionadora import routes
