from mq import Rabbitmq

def consumer(rabbit):
    rabbit.consumer(queue_name="rabbitmq_test")

if __name__== "__main__":
    rabbit = Rabbitmq()
    consumer(rabbit)