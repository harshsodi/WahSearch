# WAH Search
A full text search engine. Designed using distributed architecture for scalability and high-availability.

The system has 4 microservices but on higher level 2 major sub-systems, **crawling** and **searching**. The **Crawler** service  scrapes the web and populate the database through the **Indexer** service. On the other side, the database is used by the **Search API** which will then be accessed by the **Front End** service.
 
![](https://i.imgur.com/i75KE9s.jpg)

Each service can be run as cluster and can be scaled easily.

## Dependencies

####MongoDB
MongoDB is used as a database to store the inverted index of the web pages. The mongoDB instance must be reachable by the **Indexer**, **Crawler** and **Search API** service.

> If you are running all components on the same host, then you can just spin up a MongoDB container and connect it to the networks created by the respective service (*indexer_indexer*, *crawler_crawler* and *search_head_search_head*).
```
$ docker run -p 27017:27017 -d --name mongo mongo
```

####RabbitMQ

RabbitMQ is used as the messaging queue between **Crawler** and **Indexer**. A rabbitMQ instance reachable from the respective services is required.

> If crawler and indexer are on same host, spin up a RabbitMQ container and connect it to networks created by the services (*crawler_crawler* and *indexer_indexer*).
```
$ docker run -p 5672:5672 -d --name rabbitmq rabbitmq
```

####Redis
Redis is used as an in-memory cache while crawling to maintain the list of already visited page (distributed memoization). **Crawler** is the only service dependent on Redis so you can spin up Redis container on the same host as Crawler
```
$ docker run -p 6379:6379 -d --name redis redis
```

## Installation

Set up the MongoDB, RabbitMQ and Redis instances as and where required.
Follow instructions for installation for different components.

1. Crawler: [WAH Search - Crawler service](https://github.com/harshsodi/WahSearch/tree/master/src/crawler)
2. Indexer: [WAH Search - Indexer service](https://github.com/harshsodi/WahSearch/tree/master/src/indexer)
2. Search API: [WAH Search - Search service](https://github.com/harshsodi/WahSearch/tree/master/src/search_head)
2. Front End: [WAH Search - Front End](https://github.com/harshsodi/WahSearch/tree/master/src/front-end)

Make sure to ensure that the services run in same network as that of it's dependent services according to the dependencies mentioned above.