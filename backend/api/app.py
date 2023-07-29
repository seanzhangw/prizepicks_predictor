from flask import Flask, redirect, url_for
from apifairy import APIFairy
import os

apifairy = APIFairy()

class Config:
    # API documentation
    APIFAIRY_TITLE = 'Prizepicks Predictor API Documentation'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'rapidoc')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    apifairy.init_app(app)

    @app.route('/')
    @app.route('/api')
    def index():
        return redirect(url_for('apifairy.docs'))
    
    @app.get('/ping')
    def ping():
        return {'response': 'pong'}

    return app

