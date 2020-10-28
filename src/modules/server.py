import re

from flask import Flask, request, render_template
import json

from src.SpellSuggestion import SpellSuggestion
from src.search import Search


app = Flask(__name__, template_folder='templates')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/suggestion', methods=['GET', 'POST'])
def suggested_keywords():
    if request.method == 'GET':
        regex_word = r"[\w]+"
        # get the original string
        spell_suggestions = SpellSuggestion()
        raw_string = request.args.get("keywords")

        # checking spell and give suggestions
        raw_words = re.findall(regex_word, raw_string)  # remove non-letter chars
        words_before_spell_check = " ".join(raw_words[:-1])  # spilt the raw_string with the last space
        words_before_auto_complete = raw_words[-1]
        words_after_spell_check = None
        print("raw:{}, spell: {}, auto: {}".format(raw_words, words_before_spell_check, words_before_auto_complete))

        if words_before_spell_check:  # if more than one word typed, doing spell check and auto complete
            words_after_spell_check = spell_suggestions.spell_checker(words_before_spell_check)
        words_before_auto_complete = spell_suggestions.auto_completer(words_before_auto_complete)

        result = []
        if words_after_spell_check:
            for item in words_before_auto_complete:
                result.append(words_after_spell_check + " " + item)
        else:
            result = words_before_auto_complete
        return json.dumps(result) if result else "No results!"
    return 'Nothing Happened!'


@app.route('/search', methods=['GET', 'POST'])
def search_keywords():
    if request.method == 'GET':
        keywords = request.args.get("keywords")
        page_number_query = request.args.get("page")
        links_per_page = request.args.get("keywords")

        s = Search()
        search_results = []
        page_indexer = 1
        while True:
            if s.search(keywords, 15, page_number=page_number_query):
                print("Page NO.{}".format(page_indexer))
                for each_page_docs in s.search(keywords, 20, page_number=page_indexer):
                    print(each_page_docs)
                    search_results.append(each_page_docs)
                    page_indexer += 1

        return json.dumps(search_results)

# @app.route('/test')
# def test():
#     pager_obj = Pagination(request.args.get("page", 1), page_indexer, request.path, request.args, per_page_count=20)
#     print(request.path)
#     print(request.args)
#     index_list = li[pager_obj.start:pager_obj.end]
#     page_html_links = pager_obj.page_html()
#     print(page_html_links)
#     return render_template("test.html", index_list=index_list, html=page_html_links)


if __name__ == '__main__':
    app.run(debug=True)
