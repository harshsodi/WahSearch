import yaml
import pymongo
# import Logger

# logger = Logger.get_index_logger()

# Configure logging to log to file
# TODO: Change the log path

class MongoClient:

    def __init__(self):
        """
        Read config from config.yml
        Connect to mongodb
        Set collection objects
        """
        
        try:
            config_data = Utils.get_yaml_config_default()
            mongo_parameters = config_data.get('mongodb')
            url = mongo_parameters["url"]

            client = pymongo.MongoClient(url)
            db = client["wah_search"]
            self.db = db
            self.index = db["index"]
            self.docs = db["docs"]
        except Exception as e:
            print("Error initializing MongoDB object. Exception %s", str(e))
            raise Exception