import time

import faust
import sys

from confluent_kafka import Producer

def delivery_report(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# ------------------ Faust Stream App ------------------
app = faust.App(
    'py_stream_app',
    broker='kafka://localhost:9092',
    value_serializer='raw',
    consumer_auto_offset_reset='earliest',
)

in_topic = app.topic('test_topic')
out_topic = app.topic('test_topic_upper')

@app.agent(in_topic)
async def to_upper(stream):
    """Stream processor: read, transform, and publish to another topic."""
    async for value in stream:
        text = value.decode('utf-8')
        print(f"[stream] Received: {text}")
        transformed = text.upper()
        await out_topic.send(value=transformed.encode('utf-8'))
        print(f"[stream] Emitted:  {transformed}")

# --------- Seed producer: run ONCE at startup ----------


def produce_records():
    # Kafka producer configuration
    conf = {'bootstrap.servers': 'localhost:9092'}
    producer = Producer(conf)
    topic = 'test_topic'

    # Produce 5 messages
    for i in range(5):
        msg = f'Hello Python Kafka {i}'
        producer.produce(topic, msg.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Trigger the delivery callback immediately

    # Ensure all messages are delivered before exiting
    producer.flush()

# ------------------ Entry point ----------------------------
if __name__ == '__main__':
    produce_records()
    if len(sys.argv) == 1:
        sys.argv += ['worker', '-l', 'info']
    app.main()
