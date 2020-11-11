import json

from utils import Utils
from Indexer import Indexer
from RabbitMQ import RabbitMQ

class Worker:

    def __init__(self):
        self.indexer = Indexer()
        config = Utils.get_yaml_config_default()
        rabbitmq_ip = config["rabbitmq"]["ip"]
        self.mq = RabbitMQ(rabbitmq_ip, queue_names=['crawler_queue'])

    def run(self):
        def consume_worker(ch, method, properties, body):
            body_json = json.loads(body)
            doc_name = body_json["doc_name"]
            doc_content = body_json["doc_content"]
            self.indexer.index_html_page(doc_name, doc_content)

            ch.basic_ack(method.delivery_tag)

        self.mq.consume("html_pages", consume_worker)

w = Worker()
while True:
    w.run()