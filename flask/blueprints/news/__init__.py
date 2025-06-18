from flask import Blueprint, render_template, request
from kafka import KafkaConsumer, TopicPartition
from datetime import datetime
from babel.dates import format_datetime
import json

news = Blueprint('news', __name__, template_folder='templates')

@news.route('/')
def home_():
    return render_template('home.html')

@news.route('/news/lemonde')
def lemonde_():

    try:
        offset = int(request.args.get("offset", 0))
    except ValueError:
        offset = 0

    PAGE_SIZE = 10
    messages = []

    consumer = KafkaConsumer(
        bootstrap_servers='kafka-1:9092',
        enable_auto_commit=False,
        auto_offset_reset='earliest',
        group_id='flask-viewer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )


    partition = next(iter(consumer.partitions_for_topic('lemonde-news')))
    topic_partition = TopicPartition('lemonde-news', partition)
    consumer.assign([topic_partition])
    consumer.seek(topic_partition, offset)
    end_offset = consumer.end_offsets([topic_partition])[topic_partition]

    try:
        while len(messages) < PAGE_SIZE:
            msg = consumer.poll(timeout_ms=1000)
            if not msg:
                break
            for tp, records in msg.items():
                for record in records:
                    data = record.value

                    # Formater la date si présente
                    if 'published' in data:
                        try:
                            dt = datetime.strptime(data['published'], "%a, %d %b %Y %H:%M:%S %z")

                            # Formatage avec babel en français
                            data['published'] = format_datetime(dt, "d MMMM yyyy - HH:mm", locale='fr_FR')
                        except Exception as e:
                            print(f"⚠️ Erreur de parsing de date : {e}")

                    messages.append(data)
                    if len(messages) >= PAGE_SIZE:
                        break

    finally:
        consumer.close()

    next_offset = (offset + PAGE_SIZE)
    prev_offset = max(0, offset - PAGE_SIZE)

    return render_template(
        'lemonde.html',
        news_list=messages,
        next_offset=next_offset,
        prev_offset=prev_offset,
        offset=offset,
        has_more=offset < end_offset,
        end_offset=end_offset
    )


@news.route('/news/20minutes')
def vingtminutes_():
    try:
        offset = int(request.args.get("offset", 0))
    except ValueError:
        offset = 0

    PAGE_SIZE = 10
    messages = []

    consumer = KafkaConsumer(
        bootstrap_servers='kafka-1:9092',
        enable_auto_commit=False,
        auto_offset_reset='earliest',
        group_id='flask-viewer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )


    partition = next(iter(consumer.partitions_for_topic('20minutes-news')))
    topic_partition = TopicPartition('20minutes-news', partition)
    consumer.assign([topic_partition])
    consumer.seek(topic_partition, offset)
    end_offset = consumer.end_offsets([topic_partition])[topic_partition]

    try:
        while len(messages) < PAGE_SIZE:
            msg = consumer.poll(timeout_ms=1000)
            if not msg:
                break
            for tp, records in msg.items():
                for record in records:
                    data = record.value

                    # Formater la date si présente
                    if 'published' in data:
                        try:
                            dt = datetime.strptime(data['published'], "%a, %d %b %Y %H:%M:%S %Z")
                            # Formatage avec babel en français
                            data['published'] = format_datetime(dt, "d MMMM yyyy - HH:mm", locale='fr_FR')
                        except Exception as e:
                            print(f"⚠️ Erreur de parsing de date : {e}")

                    messages.append(data)
                    if len(messages) >= PAGE_SIZE:
                        break


    finally:
        consumer.close()

    next_offset = (offset + PAGE_SIZE)
    prev_offset = max(0, offset - PAGE_SIZE)

    return render_template(
        '20minutes.html',
        news_list=messages,
        next_offset=next_offset,
        prev_offset=prev_offset,
        offset=offset,
        has_more=offset < end_offset,
        end_offset=end_offset
    )