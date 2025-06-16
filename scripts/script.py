#!/usr/bin/env python3

import feedparser
import json
import time
from kafka import KafkaProducer
import os
import logging

# --- Configurable via variables d’environnement ---
RSS_FEEDS = [
    "https://partner-feeds.20min.ch/rss/20minutes",
    "https://www.lemonde.fr/rss/une.xml"
]

BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC =  "raw-news"
POLL_INTERVAL = 300  # secondes

# --- Kafka Producer ---
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if k else None,
    linger_ms=100,
    retries=3,
)

# --- GUID déjà vus pour ne pas renvoyer deux fois ---
seen_guids = set()

# --- Fonction principale ---
def push_entries(feed_url):
    parsed = feedparser.parse(feed_url)
    for entry in parsed.entries:
        guid = getattr(entry, "id", "") or getattr(entry, "link", "") or entry.title
        if guid in seen_guids:
            continue
        payload = {
            "feed": feed_url,
            "guid": guid,
            "title": entry.title,
            "link": entry.link,
            "published": getattr(entry, "published", None),
            "summary": getattr(entry, "summary", None),
        }
        producer.send(TOPIC, key=guid, value=payload)
        seen_guids.add(guid)
        logging.info("Envoyé : %s", entry.title)

# --- Boucle principale ---
def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    logging.info(" Démarrage : envoi RSS → Kafka topic '%s'", TOPIC)
    while True:
        for feed in RSS_FEEDS:
            try:
                push_entries(feed)
            except Exception as e:
                logging.exception("Erreur sur %s : %s", feed, e)
        producer.flush()
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Arrêté par l'utilisateur.")
    finally:
        producer.close()