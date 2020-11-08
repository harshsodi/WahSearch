import pika

from utils import Utils

class RabbitMQ:
    
    def __init__(self, ip, queue_names=[]):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip))
        self.channel = connection.channel()
        for queue_name in queue_names:
            self.init_queue(queue_name) 

    def init_queue(self, queue_name):
        """
        Initialize quque with `queue_name`if not exist    
        """
        self.channel.queue_declare(queue=queue_name)

    def publish(self, queue_name, body):
        self.init_queue(queue_name)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=body)

    def consume(self, queue_name, consume_worker):
        self.channel.basic_consume(queue=queue_name, auto_ack=False, on_message_callback=consume_worker)
        self.channel.start_consuming()

    def close_channel(self):
        self.channel.close()
