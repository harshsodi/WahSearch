"""
The engine to carry out searching through the web and publishing the html
pages to the message queue consumed by the indexer service

To maintain memoization in distributed environment,
Redis is used as a Set data-structure

Author: Harsh Sodiwala
"""

import urllib.request
import urllib.error
import urllib.parse
import urllib.robotparser
import tldextract

import urllib3
import json
import redis

from indexer import Indexer

from bs4 import BeautifulSoup
from utils import Utils
from RabbitMQ import RabbitMQ

class Spider:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    The spider that will crawl the web
    Use the given seeds and crawl through them
    Collect webpages on the way and store/index them
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    def __init__(self):
        """ 
        Constructor 
        """
        
        # Read config
        config = Utils.get_yaml_config_default()
        rabbitmq_ip = config["rabbitmq"]["ip"]
        redis_host = config["redis"]["host"]

        # Initiate RabbitMQ
        self.mq = RabbitMQ(rabbitmq_ip, queue_names=['crawler_queue'])
        
        # Initiate redis
        self.redis = redis.Redis(host=redis_host, port=6379, db = 0)

        self.indexer = Indexer()

    def get_http_response(self, url):
        """
        Send an HTTP request and return the response for given URL

        url     -- The URL of the webpage to get HTTP Response of
        return  -- HTTPRespone object
        """

        try:
            http = urllib3.PoolManager()
            http_response = http.request('GET', url)    
            print("Get_url: ", http_response.geturl())
            return http_response
        except Exception as e:
            print("Error while fetching ", url, e)
            return None

    def get_links(self, url, html_text):
        """
        Fetch links in the source code of the given page

        url         -- The url of the webpage
        html_text   -- The source code of the webpage

        return      -- String: List of links
        """

        parser = BeautifulSoup(html_text, 'html.parser') # Initialize parser
        links = parser.find_all('a') # Fetch anchor tags

        hrefs = []

        for link in links:
            href = link.get('href')
            abs_href = urllib.parse.urljoin(url, href) # Handle relative links
            abs_href = abs_href.split('#')[0] # Remove fragment identifier
            hrefs.append(abs_href)

        return hrefs

    def index_page(self, url, html_text):
        """
        Index the retrieved webpage

        url         -- URL of the webpage to index
        html_text   -- The source code of the page
        """
        
        self.indexer.index_html_page(url, html_text)

    def get_root_domain(self, url):
        extract = tldextract.extract(url)
        domain = extract.domain
        return domain

    def run(self):
        """
        The entry point
        """

        # self.domain  = self.get_root_domain(self.seeds)

        depth = 0 #initial depth
        
        def consume_worker(ch, method, properties, body):

            dtag = method.delivery_tag
            body_json = json.loads(body)
            url = body_json["url"]

            # get html response and index the page
            http_response = self.get_http_response(url)

            if not http_response: # Skip if page not retrieved
                ch.basic_nack(method.delivery_tag)
                print ("Error while getting http response for %s", url)
                return

            html_text = None
            response_url = None
            try:
                html_text = http_response.data # HTML text
                response_url = http_response.geturl() # Final URL after redirection
            except Exception:
                ch.basic_nack(method.delivery_tag)
                print ("Error while processing %s. %s", url, e)
                return

            # Add to visited set
            self.redis.sadd("visited", response_url.encode())  # mark visited links to avoid cycles in BFS
            
            try:
                self.index_page(url, html_text) # Index the retrieved webpage
            except Exception as e:
                ch.basic_nack(method.delivery_tag)
                print ("Error while indexing ", response_url, e)
                return
            
            links = self.get_links(url, html_text) # Get links from the current page

            # Push the new found links to ToCrawl list [BFS]
            external_links_threshold = 2
            for link in links:
                if not self.redis.sismember("visited", link.encode()):

                    # TODO: Figure out a way to control crawling to external domains
                    # if self.get_root_domain(url) != self.domain:
                        # external_links_threshold -= 1
                        # if external_links_threshold == 0:
                        #     break
                    
                    # Add to crawler_queue
                    self.mq.publish("crawler_queue", json.dumps({"url": link}))
                    
                    # Add to visited set
                    self.redis.sadd("visited", link.encode())

            ch.basic_ack(dtag)

        # Step into the endless loop of work.
        self.mq.consume("crawler_queue", consume_worker)
             
s = Spider()
s.run()