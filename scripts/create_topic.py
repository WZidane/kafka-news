from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(
    bootstrap_servers='kafka:9092',
    client_id='topic-creator'
)

topic_name = "raw-news"

topic = NewTopic(
    name=topic_name,
    num_partitions=1,
    replication_factor=1
)

try:
    admin_client.create_topics([topic])
    print(f"✅ Topic '{topic_name}' créé avec succès.")
except Exception as e:
    print(f"⚠️ Erreur lors de la création du topic : {e}")