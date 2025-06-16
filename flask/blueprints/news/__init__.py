from flask import Blueprint, render_template
from kafka import KafkaConsumer
from datetime import datetime
from babel.dates import format_datetime
import json

news = Blueprint('news', __name__, template_folder='templates')

@news.route('/')
def home_():
    return render_template('home.html')

@news.route('/news/lemonde')
def lemonde_():

    consumer = KafkaConsumer(
        'raw-news',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id='flask-viewer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    messages = []
    for message in consumer:
        data = message.value

        # Formater la date si présente
        if 'published' in data:
            try:
                dt = datetime.strptime(data['published'], "%a, %d %b %Y %H:%M:%S %Z")
                # Formatage avec babel en français
                data['published'] = format_datetime(dt, "d MMMM yyyy - HH:mm", locale='fr_FR')
            except Exception as e:
                print(f"⚠️ Erreur de parsing de date : {e}")

        messages.append(data)

        # On lit 10 messages et on s'arrête
        if len(messages) >= 10:
            break

    consumer.close()

    return render_template('lemonde.html', news_list=messages)