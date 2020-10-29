import nltk
import os

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

    def quick_select(self, arr, k, sort_func=None):
        
        n = len(arr)

        l = 0
        r = n - 1

        while True:
            pivot = r

            i = l
            for j in range(l, r):
                if sort_func(arr[j],arr[pivot]):
                    tmp = arr[i]
                    arr[i] = arr[j]
                    arr[j] = tmp        
                
                    i += 1

            tmp = arr[i]
            arr[i] = arr[pivot]
            arr[pivot] = tmp

            if i < k and i<n-1: # If the pointer reached the end that means there are less pages than K
                l = i+1
            elif i > k and i>0: # Same as i<n-1 condition
                r = i-1
            else:
                return (sorted(arr[:i], key=lambda x: x[0]))