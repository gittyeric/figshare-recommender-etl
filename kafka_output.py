from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "event"

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

def save_messages(txt_messages):
    last_future = None
    for msg in txt_messages:
        last_future = producer.send(TOPIC, bytes(msg, "utf-8"))

    if last_future is not None:
        last_future.get(timeout=20)
        producer.flush()
