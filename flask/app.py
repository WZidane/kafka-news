import secrets 

from datetime import datetime

from flask import Flask, session, request, redirect, url_for, jsonify

from blueprints.news import news

app = Flask(__name__, template_folder='blueprints/templates')
app.url_map.strict_slashes = False

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = secrets.token_hex(32)

app.register_blueprint(news)

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}
