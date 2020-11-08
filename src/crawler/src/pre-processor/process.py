"""
Do the pre-process jobs before launching crawler's in the open
Read from config if this is a fresh launch.
If fresh launch, reset all components to start crawling from given seeds
Else let it run from whatever state it can figure out
"""

import pymongo
import redis
import pika
import yaml
import json

# Read config
config = yaml.load(open("/opt/config.yml"), Loader=yaml.FullLoader)
settings = config["settings"]

if settings["start-fresh"]== True:
    # Clean redis set, kafka quque and mongo db
    redis_host = config["redis"]["host"]
    rabbitmq_ip = config["rabbitmq"]["ip"]
    mongo_url = config["mongodb"]["url"]

    # Clean mongo DB
    client = pymongo.MongoClient(mongo_url)
    db = client["wah_search"]
    index = db["index"].remove({})
    docs = db["docs"].remove({})

    # Clean redis set
    redis_host = redis.Redis(host=redis_host, port=6379, db = 0)
    redis_host.delete("visited")

    # Clean RabbitMQ queue and load it up with seeds for new round of crawl
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip))
    channel = connection.channel()
    channel.queue_delete(queue='crawler_queue')
    channel.queue_delete(queue='html_pages')

    channel.queue_declare(queue='html_pages')
    channel.queue_declare(queue='crawler_queue')

    # Load rabbitmq with seeds
    with open('/opt/seeds.lst') as fd:
        content = fd.read()
        data = content.split("\n")

        for url in data:
            channel.basic_publish(exchange='', routing_key='crawler_queue', body=json.dumps({"url": url}))