from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "events"

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

def save_messages(txt_messages):
    for msg in txt_messages:
        producer.send(TOPIC, bytes(msg, "utf-8"))
    producer.flush()
