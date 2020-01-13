import datetime
import os

from flask import Flask, render_template, redirect, url_for
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
