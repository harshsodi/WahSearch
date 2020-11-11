import logging

logging.basicConfig(filename='/tmp/search_head.log')
index_logger = logging.getLogger('index')

def get_index_logger():
    return index_logger