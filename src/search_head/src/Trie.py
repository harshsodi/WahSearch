"""
A fast data structure for searching strings with autocomplete support.
"""
import re
from functools import reduce
from english_words import english_words_set


# hard_disk = "./Hard_disk.txt"

class Trie(object):
    def __init__(self):
        self.children = {}
        self.flag = False  # Flag to represent that a word ends at this node

    def add(self, char):
        """ put a char in the Trie """
        self.children[char] = Trie()

    def insert(self, word):
        """ put a word in the Tire and set the existed flag as True"""
        node = self
        for char in word:
            if char not in node.children:
                node.add(char)
            node = node.children[char]
        node.flag = True

    def contains(self, word):
        """ check a word whether in the Tries, if existed return True, else return False """
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.flag

    def all_suffixes(self, prefix):
        """ get the suffix according to the given prefix """
        results = set()
        if self.flag:
            results.add(prefix)
        if not self.children: return results
        return reduce(lambda a, b: a | b,
                      [node.all_suffixes(prefix + char) for (char, node) in self.children.items()]) | results

    def autocomplete(self, prefix, top=5):
        """ return the list contains number of top words of the given prefix """
        node = self
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]
        return list(node.all_suffixes(prefix))[:top]


def words_token(text, regex=r"[\w]+"):
    """ extract all the words from text with lowercase """
    if text is not None and text != "":
        return re.findall(regex, text.lower(), re.MULTILINE)
    else:
        return ["UWindsor"]


if __name__ == '__main__':
    words = None
    test = Trie()

    # biuld the Trie from the file
    # with open(hard_disk, "r") as f:
    #     words = words_token(f.read())
    # for word in words:
    #     test.insert(word)
    #
    # print(test.autocomplete("d"))

    for word in english_words_set:
        test.insert(word)

    input_word = input("Please input a letter >> ")
    print("Did you want to type these {} ?".format(test.autocomplete(input_word)))
