from flask import Flask
from flask_cors import CORS
from app.utils.update_thread import start_update_thread

app = Flask(__name__)
CORS(app)
start_update_thread()

from app import views
from app import api