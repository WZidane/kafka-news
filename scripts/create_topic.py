from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(
    bootstrap_servers='kafka-1:9092',
    client_id='topic-creator'
)

topic_1 = NewTopic(
    name="lemonde-news",
    num_partitions=2,
    replication_factor=2
)

topic_2 = NewTopic(
    name="20minutes-news",
    num_partitions=2,
    replication_factor=2
)

try:
    admin_client.create_topics([topic_1])
    admin_client.create_topics([topic_2])
    print(f"✅ Topics créé avec succès.")
except Exception as e:
    print(f"⚠️ Erreur lors de la création du topic : {e}")