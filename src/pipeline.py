"""
"""

import sys

from multilang_analyzer import MultilangAnalyzer
from pages import *

from tqdm import tqdm

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
        articles = set()
        with tqdm(targets, total=len(targets), desc='grabbing articles from cats...') as cat_iter:
            for cat in cat_iter:
                if cat in skip_cats: continue
                cat_iter.set_postfix({
                    'cat': cat
                })
                try:
                    articles.update(get_articles(cat, self.lang))
                except:
                    print(f'could not get articles for cat {cat}')
        return list(articles)

    def save_targets(self, target_articles, filename):
        """
        saves all the target articles to a json file
        """
        with open(filename, "w") as f:
            json.dump(target_articles, f)

    def pages_full(self, targets, outfile, skip_cats=[]):
        target_articles = self.get_target_articles(targets, skip_cats)
        print('saving...')
        self.save_targets(target_articles, outfile)

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
        save dict of list of dict of sentiment data to json
        """
        with open(filename, "w") as f:
            json.dump(sentimentlist, f)

    def sentiment_full(self, infile, outfile):
        print('loading...')
        targets = self.load_targets(infile)
        sentiment_data = {}
        with tqdm(targets, total=len(targets), desc='getting page sentiment') as target_iter:
            for target in target_iter:
                try:
                    target_iter.set_postfix({
                        'target': target
                    })
                    datetextlist = self.get_all_page_edits(target)
                    sentimentlist = self.get_all_sentiment(datetextlist)
                    sentiment_data[target] = sentimentlist
                except:
                    print(f'error finding sentiment for {target}')
        print('saving...')
        self.save_sentiment(sentiment_data) 

    def load_sentiment(self, filename):
        """
        load dict of list of dict of sentiment as saved in save_sentiment
        """
        with open(filename, "r") as f:
            return json.load(f)

    def results_full(self, infile, outfile):
        print('results not yet implemented!')
        pass

