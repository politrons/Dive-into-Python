import time
import faust
import sys
from confluent_kafka import Producer

# Delivery callback for the synchronous test producer below.
# It reports success/failure per message once the broker acks it.
def delivery_report(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# ------------------ Faust Stream App ------------------
# Notes:
# - Use "faust-streaming" (the maintained fork) for Python 3.9+ compatibility.
# - The broker URI uses the "kafka://" scheme for Faust.
# - consumer_auto_offset_reset='earliest' helps during testing so you can
#   see messages that were produced before the consumer first ran,
#   provided the consumer group has no committed offset yet.
app = faust.App(
    'py_stream_app',                       # also used as the consumer group id
    broker='kafka://localhost:9092',       # KRaft/ZooKeeper-less Kafka is fine
    value_serializer='raw',                # work with bytes
    consumer_auto_offset_reset='earliest',
)

# Input topic (consumed by the agent) and output topic (where we publish results).
in_topic = app.topic('test_topic')
out_topic = app.topic('test_topic_upper')

@app.agent(in_topic)
async def to_upper(stream):
    """Consume bytes from test_topic, uppercase them, and publish to test_topic_upper."""
    async for value in stream:
        text = value.decode('utf-8')
        print(f"[stream] Received: {text}")
        transformed = text.upper()
        await out_topic.send(value=transformed.encode('utf-8'))
        print(f"[stream] Emitted:  {transformed}")

# ------------------ Test Producer ------------------
# This is a simple synchronous producer that runs before the Faust worker starts.
# It is useful for seeding data quickly during development.
def produce_records():
    conf = {'bootstrap.servers': 'localhost:9092'}
    producer = Producer(conf)
    topic = 'test_topic'

    # Produce a few test messages and trigger delivery callbacks.
    for i in range(5):
        msg = f'Hello Python Kafka {i}'
        producer.produce(topic, msg.encode('utf-8'), callback=delivery_report)
        producer.poll(0)

    # Ensure all in-flight messages are acknowledged before exiting.
    producer.flush()

# ------------------ Entry point ------------------
# Execution model:
# 1) Produce a handful of messages synchronously.
# 2) Start the Faust worker in the same process using app.main() (CLI-equivalent).
#    Faust manages its own asyncio loop; do not wrap app.main() in asyncio.run().
if __name__ == '__main__':
    produce_records()

    # If no CLI args were provided, default to "worker -l info" like `faust -A app worker -l info`.
    if len(sys.argv) == 1:
        sys.argv += ['worker', '-l', 'info']

    app.main()
