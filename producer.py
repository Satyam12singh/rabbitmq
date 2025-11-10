from mq import Rabbitmq

def producer(rabbit, message):
    rabbit.producer(queue_name="rabbitmq_test",body = message )

if __name__== "__main__":
    rabbit = Rabbitmq()
    try:
        while True:
            message = input("message to sent in queue (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            producer(rabbit, message)
    finally:
        if rabbit.producer_connection:
            rabbit.producer_connection.close()