# Search service

Host the front end (ReactJS). NPM servers runs on multiple nodes behind a load-balancer (HA Proxy).  
 
![](https://i.imgur.com/ysYCJC5.jpg)

## Requirements
- This is a containerized application and would require **Docker** and 
**docker-compose** to run.

## Installation

1. Update the search API URL address in **config.json**
    ```
    {
        "config": {
            "api_url": "http://<search_api>:<port>"
        }
    }
    ```
2. Run docker-compose. Specify the number of worker nodes in **--scale worker=**
    ```bash
    $ docker-compose up -d --scale worker=3
    ```

The web application can then be accessed on port **9090** (load-balancer/proxy) by the user.