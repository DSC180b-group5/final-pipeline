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

def plot(df, p, X, y, name):
    ax = df.plot(x='year', y=y, kind='scatter')
    ax.plot(X, p.const + p.year * X)
    ax.set_xlim([2000, 2022])
    ax.set_ylim([round(df[y].min()-0.1, 1), round(df[y].max()+0.1, 1)])
    fig = ax.get_figure()
    fig.savefig(name)
  
def results(data, language):
  """
  outputs a fixed effects regression summary of the sentiment scores
  """
  df = pd.DataFrame.from_dict(data, orient='index')
  new_df = to_dataframe(df)
  dum = pd.get_dummies(new_df['article name'], drop_first=True)
  new_df = new_df.join(dum).drop('article name', axis=1)
  cols = list(new_df.columns)
  cols.remove('avg_sentiment')
  cols.remove('med_sentiment')
  Y = new_df['avg_sentiment']
  X = new_df[cols]
  X = sm.add_constant(X)
  model = sm.OLS(Y,X)
  results = model.fit()
  p = results.params
  plot(new_df, p, X, 'avg_sentiment', name=f"data/{language}_avg_sentiment.png")
  Y2 = new_df['med_sentiment']
  model2 = sm.OLS(Y2,X)
  results2 = model2.fit()
  p2 = results2.params
  plot(new_df, p2, X, 'med_sentiment', name=f"data/{language}_med_sentiment.png")
  return results.summary(), results2.summary()
