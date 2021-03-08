import pandas as pd
import statsmodels.api as sm
       
def to_year(string):
  """
  input is a timestamp (string)
  outputs the year portion from timestamp as an integer
  """
    year = string[0:4]
    return int(year)

def to_dataframe(df):
  """
  input is the sentiment scores converted from a json file to a dataframe
  output is a dataframe consisting of three columns: year, average sentiment score of an article for a particular year, and the name of the article
  """
    dflist = []
    for i in range(len(df)):
        mini = df.iloc[i].dropna()
        time = []
        sentiment = []
        for j in range(len(mini)):
            time.append(mini[j]['time'])
            sentiment.append(mini[j]['sentiment'])
        dfn = pd.DataFrame({'time': time, 'sentiment': sentiment})
        dfn['time'] = dfn['time'].apply(to_year)
        dfn = (
            dfn.groupby('time')['sentiment']
            .agg(["mean", "median"])
            .reset_index()
            .rename(columns={
                "time": "year", 
                "mean": "avg_sentiment", 
                "median": "med_sentiment"
            })
        )
        dfn['article name'] = mini.name
        dflist.append(dfn)
    new_df = pd.concat(dflist, ignore_index=True)
    return new_df
  
def results(data):
  """
  outputs a fixed effects regression summary of the sentiment scores
  """
  df = pd.DataFrame.from_dict(data, orient='index')
  new_df = to_dataframe(df)
  dum = pd.get_dummies(new_df['article name'], drop_first=True)
  new_df = new_df.join(dum).drop('article name', axis=1)
  cols = list(new_df.columns)
  cols.remove('avg_sentiment')
  Y = new_df['avg_sentiment']
  X = new_df[cols]
  X = sm.add_constant(X)
  model = sm.OLS(Y,X)
  results = model.fit()
  p = results.params
  return results.summary()
