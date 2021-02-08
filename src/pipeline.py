"""
"""

import sys

sys.path.insert(0, 'multilanguage-sentiment-analyzer')


from multilang_analyzer import MultilangAnalyzer
from pages import *

class WikiPipeline:

    """
    USAGE

    #TODO
    """

    def __init__(self, lang):
        self.analyzer = MultilangAnalyzer(lang)
        self.lang = lang
        self.analyzer.setup()

    def get_target_articles(self, targets, skip_cats = []):
        """
        returns a list of all the articles in the target categories
        """
        pass #TODO

    def save_targets(self, target_articles, filename):
        """
        saves all the target articles to a json file
        """
        with open(filename, "w") as f:
            json.dump(target_articles, f)

    def load_targets(self, filename):
        """
        loads list of targets as saved from save_targets
        """
        with open(filename, "r") as f:
            return json.load(f)

    def get_all_page_edits(self, name):
        """
        acquires all versions of the given page, in a list of dicts

        url -> [{time, text}, {time, text} ...]    
        """
        return get_history(name, self.lang)

    def sentiment(self, text):
        return self.analyzer.sentiment(text)

    def get_all_sentiment(self, datetextlist):
        """
        given output from get_all_page_edits, get sentiment for each text
        output in the form of tuples (date, sentiment)

        [{time, text}, {time, text} ...] ->  [{time, sentiment}, {time, sentiment} ...]
        """
        return [{'time': item['time'], 'sentiment': self.sentiment(item['text'])} 
                for item in datetextlist.items()]

    def save_sentiment(self, sentimentlist, filename):
        """
        save list of dict of sentiment data to json
        """
        with open(filename, "w") as f:
            json.dump(sentimentlist, f)

    def load_sentiment(self, filename):
        """
        load list of dict of sentiment as saved in save_sentiment
        """
        with open(filename, "r") as f:
            return json.load(f)

