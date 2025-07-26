from confluent_kafka import Producer

def delivery_report(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def main():
    conf = {'bootstrap.servers': 'localhost:9092'}
    producer = Producer(conf)

    topic = 'test_topic'
    for i in range(5):
        msg = f'Hello Python Kafka {i}'
        producer.produce(topic, msg.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # trigger delivery callback

    producer.flush()

if __name__ == '__main__':
    main()
