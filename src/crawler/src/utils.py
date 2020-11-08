import nltk
import os
import yaml

class Utils:

    def __init__(self):
        self.load_stop_words()

    def load_stop_words(self):
        try:
            dir_path = self.get_project_root()
            file_path = os.path.join(dir_path, 'src', 'stop_words.dat')
            stop_words_file = open(file_path)
            stop_word_data = stop_words_file.read()
            stop_words_list = stop_word_data.split('\n')

            self.stop_words = dict.fromkeys(stop_words_list, True)
            self.stemmer = nltk.SnowballStemmer("english")
        
        except Exception:
            print ("Error while loading processing engine. WIll index useless stuff along with useful ones.")


    def get_project_root(self):
        """Returns project root folder."""
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_processed_words_list(self, words):

        """
        Process words list and return a searchable words list
        remove stop words
        stem remaining words
        """

        processed_list = []

        for word in words:
            if not self.stop_words.get(word):
                word = self.stemmer.stem(word)
                processed_list.append(word)

        return processed_list
    
    def get_yaml_config_default():
        
        config_path = "/opt/config.yml"

        try:
            yaml_data = yaml.load(open(config_path), Loader=yaml.FullLoader)
            return yaml_data
        except Exception as e:
            print ("Error while loading config from %s. \n%s", config_path, e)