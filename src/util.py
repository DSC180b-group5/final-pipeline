import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def get_history(article_name):
    '''
    Return all the text and corresponding time of one article given article_name.
    
    Example:
    article_history = get_history('Gigantorhynchus')
    article_history.head()
    '''
    
    # Get the page
    response = requests.get(
        url="https://en.wikipedia.org/w/index.php?title=Special:Export&pages={}&history=1&action=submit+".format(article_name),
    )
    soup = BeautifulSoup(response.content, 'html.parser')
    data = []
    
    #Get all the data
    for rev in soup.find_all('revision'):
        text = rev.text
        
        # Trying to remove anything before the real text (but it doesn't apply to every circumstance).
        # This line of code will remove XXXX{{XXXXX}} in the begining. 
        # TODO!
        #text = re.sub('[^\{]*\{\{[^\{]*\}\}', '', text)
        
        # Remove unimportant punctuations 
        text = re.sub('[\[\]\n\']', '', text)
        
        data.append({'time': rev.timestamp, 'text': text})

    return pd.DataFrame(data)
 

def compute_sent(input_file, out_folder, sent_func):
    '''
    From given csv file, get all the edit history for all the pages and compute the corresponding sentiment scores.
    
    
    Example:
    
    def fake_senti(x):
        return len(x)
    compute_sent('/data/article_lists/en/en_Cross-dressing.csv', '/output/en', fake_senti)
    '''
    
    
    #Get the list of articles
    df = pd.read_csv(input_file, index_col = 0)
    
    for i in range(len(df)):
        # Get history of one page
        hist = get_history(df.title[i])
        
        # Compute sentiments
        # TODO: SHOULD BE CHANGED ACCORDING TO SENTIEMNT ANALYSIS METHOD
        sents = hist.text.apply(fake_senti)
        hist['sentiments'] = sents
        
        # Save to output file
        hist.save_csv(out_folder + '/' + df.title[i] + '.csv')
        

def get_cat(cmtitle, lang):
    '''
    Query by using category name and return all the pages or subcategories in the result. 
    '''
    
    
    S = requests.Session()

    URL = "https://{}.wikipedia.org/w/api.php".format(lang)

    PARAMS = {
        "action": "query",
        "cmtitle": cmtitle,
        "cmlimit": "max",
        "list": "categorymembers",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    try:
        PAGES = DATA['query']['categorymembers']
        return PAGES
    except:
        return 0

def get_articles(cat_name, lang):
    '''
    Given the name of a category, return all the articles inside the category. 
    '''    
    i = 0
    PAGES = get_cat(cat_name, lang)
    all_cat = [cat_name]
    articles = []
    
    if lang == 'es':
        CATEGORY = 'Categoría'
    else:
        CATEGORY = 'Category'
        
    while len(PAGES) > 0:
        p = PAGES[0]
        PAGES = PAGES[1:]
        if CATEGORY in p['title']:
            if p['title'] in all_cat:
                continue
            TEMP_P = get_cat(p['title'], lang)
            all_cat.append(p['title'])
            if TEMP_P == 0:
                continue
            else:
                PAGES += TEMP_P
        else:
            articles.append(p)
            i += 1
            if i % 1000 == 0:
                print("{} articles done".format(str(i)))
    return pd.DataFrame(articles).drop_duplicates().reset_index(drop = True)
  
  
def iter_cats(cat_name, out_path, skip_cats = [], lang = 'en'):
    '''
    Get all the articles for each subcategory of one given category. 
    The results are saved in different csv files corresponding to category names.
    
    skip_cats: a list of categories that you want to skip    
    '''
    
    PAGES = get_cat(cat_name, lang)
    finished_cat = skip_cats
    
    if lang == 'es':
        CATEGORY = 'Categoría'
    else:
        CATEGORY = 'Category'

    ind = len(CATEGORY) + 1    
    
    for p in PAGES:
        if CATEGORY in p['title'] and not p['title'] in finished_cat:
            start = time.time()
            print(p['title'])
            article = get_articles(p['title'], lang)
            outfile = out_path + lang + '_' + p['title'].strip()[ind:] + '.csv'
            article.to_csv(outfile)
            finished_cat.append(p['title'])
            print(time.time() - start)
