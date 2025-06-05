import secrets
from flask import Flask, session, request, redirect, url_for, jsonify

from blueprints.home import home

app = Flask(__name__, template_folder='blueprints/templates')
app.url_map.strict_slashes = False

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = secrets.token_hex(32)

app.register_blueprint(home)