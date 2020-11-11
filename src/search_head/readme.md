# Search service

Serves the search API (Flask). Flash servers runs on multiple nodes behind a load-balancer (HA Proxy).  
 
![](https://i.imgur.com/4sziajg.jpg)

## Requirements
- This is a containerized application and would require **Docker** and 
**docker-compose** to run.
- A **MongoDB** installation is required. If you have already set up the Indexer service, you must have it running already. Use the same instance here.
It is recommended that you set up the mongo-db instance on the same network as the search service. An easy way is to spin a **mongo** container and attach it to the network `search_head_search_head` that would be created by the **docker-compose**.
    &nbsp;
    ```bash
    $ docker run -p 27017:27017 --name <container_name> --network search_head_search_head mongo
    ```
    This can then be reached by the container name instead of IP.

## Installation

1. Update the mongo-db address in **config.yml**
    ```
    mongodb:
        url: mongodb://<mongo_url>:27017
    ```
2. Run docker-compose. Specify the number of worker nodes in **--scale search-head=**
    ```bash
    $ docker-compose up -d --scale search_head=3
    ```

The API can then be accessed on port **8080** by the front-end service 