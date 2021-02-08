"""
Multi-language sentiment analyzer
meant to take advantage of multiple NLPs while simplifying downstream analysis code
"""

from snownlp import SnowNLP
from pysentimiento import SentimentAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer as VADER

DEFAULT_TEXT = u'.'

class MultilangAnalyzer:

    """
    USAGE

    declare analyzer:
    mlyzer = MultilangAnalyzer("EN")

    setup analyzer:
    mlyser.setup() # TODO: do we need this step? what args would we need?

    use analyzer:
    mlyser.sentiment(text)
    """

    def __init__(self, lang):
        """
        lang: language code
        """

        SETUP_FXNS = {
            'EN': self.__setup_en,
            'ES': self.__setup_es,
            'ZH': self.__setup_zh
        }

        SENTIMENT_FXNS = {
            'EN': self.__sentiment_en,
            'ES': self.__sentiment_es,
            'ZH': self.__sentiment_zh
        }

        self.lang = lang

        self.setup = SETUP_FXNS[lang]
        self.sentiment = SENTIMENT_FXNS[lang]

    """
    ### SETUP METHODS ###
    """ 
    
    def __setup_en(self):
        self.analyzer = VADER()
        

    def __setup_es(self):
        self.analyzer = SentimentAnalyzer()

    def __setup_zh(self):
        self.analyzer = SnowNLP(DEFAULT_TEXT)

    """
    ### SENTIMENT METHODS ###
    """ 

    def __sentiment_en(self, text):
        return self.analyzer.polarity_scores(text)

    def __sentiment_es(self, text):
        return self.analyzer.predict_probas(text)

    def __sentiment_zh(self, text):
        self.analyzer.doc = text
        return self.analyzer.sentiments
