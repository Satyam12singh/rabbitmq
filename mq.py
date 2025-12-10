import pika
from dotenv import load_dotenv
import os
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials
import logging
load_dotenv()

logging.getLogger(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(base_path, 'logs/mq.log'), level=logging.INFO)


host = os.getenv("RABBIT_MQ_HOST")
port = os.getenv("RABBIT_MQ_PORT")
user = os.getenv("RABBIT_MQ_USER")
password = os.getenv("RABBIT_MQ_PASSWORD")

class Rabbitmq():
    def __init__(self):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.producer_connection = None
        self.producer_channel = None

    def connection_establish(self):
        while True:
            try:
                credentials = PlainCredentials(self.user, self.password, erase_on_connect=False)
                connection = ConnectionParameters(
                    self.host,
                    self.port,
                    credentials=credentials,
                    heartbeat=600
                )
                return pika.BlockingConnection(connection)
            except Exception as e:
                logging.info(f"Error connecting to RabbitMQ: {e}")
                logging.info("Reconnecting to RabbitMQ...")
                time.sleep(5)

    def callback(self, ch, method, properties, body):
        message = body.decode('utf-8')
        logging.info(f"recieved: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consumer(self, queue_name):
        try:
            connection = self.connection_establish()
            consumer_ch = connection.channel()

            consumer_ch.queue_declare(queue=queue_name, durable=True)

            logging.info(f"starting to listen queue {queue_name}")
            consumer_ch.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=False)
            consumer_ch.start_consuming()
            

        except pika.exceptions.AMQPConnectionError as e:
            logging.info(f"Error connecting to RabbitMQ: {e}")
        except KeyboardInterrupt:
            logging.info("Consumer stopped by user.")

    def check_connection(self, queue_name):
        try:
            conn = self.connection_establish()
            ch = conn.channel()

            ch.queue_declare(queue=queue_name, passive=True)
            logging.info(f"Queue '{queue_name}' exists.")
            return True

        except pika.exceptions.ChannelClosedByBroker:
            logging.info(f"Queue '{queue_name}' does NOT exist.")
            return False

    def producer_body(self, queue_name, body):
        try:
            # If channel is usable, send directly
            if self.producer_channel and self.producer_channel.is_open:
                self.producer_channel.basic_publish(exchange='', routing_key=queue_name, body=body)
                logging.info(f"message sent: {body}")
                return

            # Else recreate connection and channel
            self.producer_connection = self.connection_establish()
            self.producer_channel = self.producer_connection.channel()

            self.producer_channel.queue_declare(queue=queue_name, durable=True)
            self.producer_channel.basic_publish(exchange='', routing_key=queue_name, body=body)
            logging.info(f"message sent: {body}")

        except Exception as e:
            logging.info(f"Error producing message: {e}")

    def producer(self, queue_name, body):
        try:
            queue_exists = self.check_connection(queue_name)

            if not queue_exists:
                logging.info(f"Creating queue '{queue_name}' before sending...")
                conn = self.connection_establish()
                ch = conn.channel()
                ch.queue_declare(queue=queue_name, durable=True)

            self.producer_body(queue_name, body)

        except pika.exceptions.AMQPConnectionError as e:
            logging.info(f"Error connecting to RabbitMQ: {e}")
        except KeyboardInterrupt:
            logging.info("Producer stopped by user.")

    def close(self):
        try:
            if self.producer_channel and self.producer_channel.is_open:
                self.producer_channel.close()
            if self.producer_connection and self.producer_connection.is_open:
                self.producer_connection.close()
        except Exception as e:
            logging.info(f"Error closing connection: {e}")
