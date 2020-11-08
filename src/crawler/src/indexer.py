"""
To handle the indexing of the pages/documents

Author: Harsh Sodiwala
"""

import re
import nltk
import math
import functools
import json
import utils

from bs4 import BeautifulSoup
from RabbitMQ import RabbitMQ

class Indexer:

    def __init__(self):
        """
        Constructor
        """

        self.utils = utils.Utils()
        config = utils.Utils.get_yaml_config_default()
        rabbit_ip = config["rabbitmq"]["ip"]
        self.mq = RabbitMQ(rabbit_ip, 'html_pages')

    def index_html_page(self, doc_name, doc_content):
        """
        Send the doc data to messagin queue [RabbitMQ]
        """
        
        content = {
            "doc_name": doc_name,
            "doc_content": doc_content.decode()
        }
        self.mq.publish('html_pages', json.dumps(content))

if __name__ == "__main__":
    #test
    sample_file_path = '../../sample_data/Accessible Rich Internet Applications (WAI-ARIA) 1.0.htm'

    file = open(sample_file_path, 'r')
    data = file.read()
    file.close()

    indexer = Indexer()
    indexer.index_html_page("www.example2.com", data)