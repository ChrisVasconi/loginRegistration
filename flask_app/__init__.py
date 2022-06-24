from flask_bcrypt import Bcrypt
from flask import Flask


app = Flask(__name__)
app.secret_key = 'secret'

DATABASE = "login_register.schema"

bcrypt = Bcrypt(app)
