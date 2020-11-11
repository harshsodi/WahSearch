"""
To handle the indexing of the pages/documents

Author: Harsh Sodiwala
"""

import re
import nltk
import math
import functools

import utils

from bs4 import BeautifulSoup

class Indexer:

    def __init__(self):
        """
        Constructor
        """

        self.load_mongo_client()
        self.utils = utils.Utils()

    def load_mongo_client(self):
        """
        Load the mongoDB handler
        """

        import pymongo
        
        config = utils.Utils.get_yaml_config_default()
        mongo_url = config["mongodb"]["url"]

        myclient = pymongo.MongoClient(mongo_url)
        mydb = myclient["wah_search"]
        self.index = mydb["index"]
        self.docs = mydb["docs"]

    def index_words(self, words, doc_name, title, h1, h2, h3, h4):

        # Generate table with word frequence
        word_dict = {}

        # Populate word dictionary
        all_words = self.utils.get_processed_words_list(words)
        for word in all_words:
            word_dict[word] = word_dict.get(word,0) + 1
        
        # Calculate normalizing factor: Root of sum of squares of word frequencies
        normalizing_factor = 0.0
        for word in word_dict:
            normalizing_factor += math.pow(word_dict[word], 2)
        normalizing_factor = math.sqrt(normalizing_factor)

        normalizing_factor = len(all_words)

        print ("Normalizer: ", normalizing_factor)

        for word in word_dict:
            cnt = word_dict[word]
            query = {"word":word}

            # upd = {"$push": {word: {docId: count}}}
            upd = dict()
            upd["$push"] = dict()
            upd["$push"]["doc_list"] = {
                "doc_id": doc_name,
                "doc_title": title,
                "frequency": cnt,
                "frequency_normalized": cnt / normalizing_factor
            }

            # Append the page with count to the word->doc list
            update_status = self.index.update(query, upd)
            updated = update_status.get('updatedExisting')

            # If the word is seen first time
            if not updated:
                upd = dict()
                upd["word"] = word
                upd["doc_list"] = [{"doc_id": doc_name, "doc_title": title, "frequency": cnt, "frequency_normalized": cnt / normalizing_factor}]
                
                self.index.insert(upd)

    def update_doc_list(self, doc_name):
        q = {"lst": {"$exists": True}}
        if self.docs.find(q).count():
            if not self.docs.find({"lst": doc_name}).count():
                self.docs.update({}, {"$inc": {"cnt": 1}})
                self.docs.update({}, {"$addToSet": {"lst": doc_name}})

        else:
            self.docs.insert({
                    "cnt":1,
                    "lst": [doc_name]
            })

    def index_html_page(self, doc_name, doc_content):
        """
        Parse the HTML page, fetch keywords and index them

        doc_name    - The reference (URL) to the page
        doc_content - THe HTML content of the page
        """

        doc_content = doc_content.lower()
        parser = BeautifulSoup(doc_content, 'html.parser') # Initialize parser

        # Get title
        title = ""
        title_tag = parser.find('title')
        if title_tag:
            title = title_tag.text

        # Keep title and body words separate for now
        # TODO - Implementing word weightage in future

        # Get whole body part in text
        body = ""
        body_tag = parser.find('body')
        if title_tag:
            body = body_tag.text

        non_alpha_num_exp = r'[^a-z0-9 ]' # Regex: Everything except aplhanumeric characters

        # Get headings
        h1_list = parser.find_all("h1") * 5
        h2_list = parser.find_all("h2") * 4
        h3_list = parser.find_all("h3") * 3
        h4_list = parser.find_all("h4") * 2

        h1 = " ".join(map(lambda x: x.text, h1_list)).split()
        h2 = " ".join(map(lambda x: x.text, h2_list)).split()
        h3 = " ".join(map(lambda x: x.text, h3_list)).split()
        h4 = " ".join(map(lambda x: x.text, h4_list)).split()
        
        original_title = title.capitalize()
        title = re.sub(non_alpha_num_exp,' ', title)
        body = re.sub(non_alpha_num_exp,' ', body) # Replace non alphanumeric characters with space
        # TODO - Take care of words that become like randomword34 after replacement

        # Get list of words from both
        title_words = title.strip().split() * 10 # Title words are more important than body words
        body_words = body.strip().split()
        all_words = title_words + body_words + h1 + h2 + h3 + h4

        # Insert in the inverted index
        self.index_words(all_words, doc_name, original_title, h1, h2, h3, h4)
        self.update_doc_list(doc_name)

if __name__ == "__main__":
    #test
    sample_file_path = '../../sample_data/Accessible Rich Internet Applications (WAI-ARIA) 1.0.htm'

    file = open(sample_file_path, 'r')
    data = file.read()
    file.close()

    indexer = Indexer()
    indexer.index_html_page("www.example2.com", data)