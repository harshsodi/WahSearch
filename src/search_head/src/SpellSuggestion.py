"""
class SpellSuggestion do spell check and auto complete with raw keywords
suggestion
"""
import re
import string
from collections import Counter
from Trie import Trie

english_words = "./words_alpha.txt"


class SpellSuggestion(object):
    def __init__(self, regex=r"[\w]+"):
        """ initialize the WORDS dictionary which the key is a word and the value is the occurrences of the key  """
        self.trie = Trie()
        self.regex = regex

        with open(english_words, "r") as f:  # Create a dictionary for storing all the words and its occurrences
            self.WORDS = Counter(self.words_token(f.read()))

        for word in self.WORDS.keys():  # put all the words in Trie
            self.trie.insert(word)

    def words_token(self, text):
        """ extract all the words from text with lowercase """
        if text is not None and text != "":
            return re.findall(self.regex, text.lower(), re.MULTILINE)
        else:
            return ["UWindsor"]

    def probability_of_word(self, word):
        """ calculate the probability of a given word """
        # return self.WORDS[word] / len(self.WORDS.values())
        return self.WORDS[word] / sum(self.WORDS.values())

    def edit_distance_1(self, word):
        """ get all combinations from the given word which edit distance is 1 """
        letters = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(replaces + deletes + transposes + inserts)

    def edit_distance_2(self, word):
        """ get all combinations from the given word which edit distance is 2 """
        return set(e2 for e1 in self.edit_distance_1(word) for e2 in self.edit_distance_1(e1))

    def shown(self, words):
        """ return words that are shown in WORDS based on edit distance which is ether 1 or 2 """
        return set(w for w in words if w in self.WORDS)

    def candidates(self, word):
        """ get all the candidate words from the given word """
        return self.shown([word]) or self.shown(self.edit_distance_1(word)) or self.shown(self.edit_distance_2(word)) or [word]

    def correct_word(self, word) -> str:
        """ get the most probable word suggestion for the given word """
        return max(self.candidates(word), key=self.probability_of_word)

    def spell_checker(self, words) -> str:
        """ check all the words and return the words with modifications """
        tokens = self.words_token(words)
        return " ".join([self.correct_word(token) for token in tokens])

    # def spell_checker(self, word):
    #     """ get the most probable spelling suggestion for the given word. """
    #     # return sorted(self.candidates(word), key=self.probability_of_word)[0]
    #     return max(self.candidates(word), key=self.probability_of_word)

    def auto_completer(self, prefix, top=5):
        """ return number of top auto complete suggestion according the prefix """
        return self.trie.autocomplete(prefix, top)  # get the top word accourding to the given prefix


if __name__ == '__main__':
    raw_strings = ["master of comp"]

    print("*" * 30)
    test = SpellSuggestion()
    # test.probability_of_word("the")
    # input_word = input("Please type a keyword >>> ")
    # print("Did you mean: {} or still use {} ?".format(test.spell_checker(input_word), input_word))

    regex_word = r"[\w]+"
    for raw_string in raw_strings:
        print("raw words: {}".format(raw_string))
        raw_words = re.findall(regex_word, raw_string)  # remove non-letter chars
        words_for_spell_checker = " ".join(raw_words[:-1])  # spilt the raw_string with the last space
        words_for_auto_completer = raw_words[-1]
        if words_for_spell_checker: # if user type a space, then check the form words
            print("Spell checker: {}".format(test.spell_checker(words_for_spell_checker)))
        print("Suggestions: {} \n".format(test.auto_completer(words_for_auto_completer)))

