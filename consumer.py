from kafka import KafkaConsumer
consumer = KafkaConsumer('test-topic', bootstrap_servers='10.11.31.193:9092')
for msg in consumer:
    print(msg.value.decode())