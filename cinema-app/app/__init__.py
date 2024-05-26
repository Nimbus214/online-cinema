from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'each-scythian-has-an-altushka'

from app import routes