# Indexer
 
![](https://i.imgur.com/DniLxxX.jpg)

## Requirements
- This is a containerized application and would require **Docker** and 
**docker-compose** to run.
- The **MongoDB**, **Redis** and **RabbitMQ** instances must be reachable from crawler host. (The **Docker network** is ```indexer_indexer```)

## Installation

1. Update the mongo-db, redis and rabbitmq config in **config.yml**
    ```
    rabbitmq:
        ip: rabbitmq

    mongodb:
        url: mongodb://mcont:27017
    ```
2. Run docker-compose. Specify the number of worker nodes in **--scale indexer=**
    ```bash
    $ docker-compose up -d --scale indexer=6
    ```
    
The worker containers will then start consuming the queue ```html_pages``` (url's to fetch) from the **RabbitMQ** instance and process the html_content and index it to **MongoDB**. The front-wnd will use this MongoDB instance for search query processing.