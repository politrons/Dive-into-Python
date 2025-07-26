import asyncio
from confluent_kafka import Producer
from confluent_kafka import Consumer

# Callback function to report the result of each message delivery.
def delivery_report(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Asynchronous function to consume messages from a Kafka topic.
async def consume_records():
    # Kafka consumer configuration
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'earliest',
    }

    # Create and subscribe the consumer to the target topic
    consumer = Consumer(conf)
    consumer.subscribe(['test_topic'])
    print("Listening for messages...")

    try:
        while True:
            # Poll for new messages with a 1-second timeout
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
            else:
                # Decode and print the received message
                print(f"Received message: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    finally:
        # Always close the consumer on exit
        consumer.close()

# Function to produce several messages to a Kafka topic.
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

# Main entry point of the script
if __name__ == '__main__':
    # Start the consumer coroutine
    async_consumer = consume_records()

    # Produce messages synchronously
    produce_records()

    # Run the asynchronous consumer
    asyncio.run(async_consumer)
