from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='10.11.31.193:9092')
producer.send('test-topic', b'Hello from Python')
producer.flush()