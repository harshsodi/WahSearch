import yaml
import pymongo
import Logger
import os

logger = Logger.get_index_logger()

# Configure logging to log to file
# TODO: Change the log path

class MongoClient:

    def __init__(self):
        """
        Read config from config.yml
        Connect to mongodb
        Set collection objects
        """

        config_file_path = os.path.join(os.environ["ROOT_PATH"], "config.yml")
        
        try:
            with open(config_file_path) as fd:
                config_data = yaml.load(fd, Loader=yaml.FullLoader)
                mongo_parameters = config_data.get('mongodb')
                url = mongo_parameters["url"]
                client = pymongo.MongoClient(url)
                db = client["wah_search"]
                self.index = db["index"]
                self.docs = db["docs"]
        except Exception as e:
            print (e)
            logger.error("Error initializing MongoDB object. Exception %s", str(e))
            raise Exception