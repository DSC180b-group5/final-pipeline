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
        self.analyzer.setup()

    def get_page(self, url):
        pass #TODO

    def get_edit(self, TODO):
        #TODO args - what do we need to get a specific edit?
        pass

    def get_all_page_edits(self, url):
        """
        acquires all versions of the given page, in a list of tuples
        where each tuple is the date of the edit and the text of the article

        url -> [(date, text), (date, text) ...]    
        """
        pass #TODO

    def sentiment(self, text):
        return self.analyzer.sentiment(text)

    def get_all_sentiment(self, datetextlist):
        """
        given output from get_all_page_edits, get sentiment for each text
        output in the form of tuples (date, sentiment)

        [(date, text), (date, text) ...] ->  [(date, sentiment), (date, sentiment) ...]
        """
        return [(date, self.sentiment(text)) for date, text in datetextlist]
