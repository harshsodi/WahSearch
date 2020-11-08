# Crawler
 
![](https://i.imgur.com/8gfvBxs.jpg)

## Requirements
- This is a containerized application and would require **Docker** and 
**docker-compose** to run.
- The **MongoDB**, **Redis** and **RabbitMQ** instances must be reachable from crawler host. (The **Docker network** is ```crawler_crawler```)

## Installation

1. Update the mongo-db, redis and rabbitmq config in **config.yml**
    ```
    rabbitmq:
        ip: rabbitmq

    mongodb:
        url: mongodb://mcont:27017

    redis:
        host: redis
    ```
2. Update the ```start-fresh``` parameter in **config.yml**. Set it true to crawl from the scratch using seeds given in **seeds.lst** and False to resume crawling as per the state of the message queue and redis cache.
    ```
    settings:
        start-fresh: True
    ```
    Update the **seeds.lst** file if required
    ```
    https://www.w3schools.com
    https://www.tutorialspoint.com
    https://www.geeksforgeeks.org/
    https://www.tutorialspoint.com/index.htm
    ```

3. Run docker-compose. Specify the number of worker nodes in **--scale worker=**
    ```bash
    $ docker-compose up -d --scale worker=6
    ```
    This will first run a ```pre-process``` container which will clean up the state of crawling as per the parameter ```start-fresh``` in config.

The worker containers will then start consuming the queue ```crawler_queue``` (url's to fetch) from the RabbitMQ instance and publish the processed pages to ```html_pages``` queue which will then be consumed by the Indexer service. The visited pages are tracked in a _set data structure_ in the **Redis** instance.