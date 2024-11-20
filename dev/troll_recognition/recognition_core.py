import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

import multiprocess as mp
import gc
from catboost import CatBoostClassifier

from sklearn.base import BaseEstimator, TransformerMixin

def percentile_calc(data, groupby_col, num_cols, percentile_list):
    non_numeric = [col_name for col_name in data.columns if col_name not in num_cols]
    for qu in percentile_list: 
        percentiles = data.groupby(groupby_col).quantile(q=qu/100).reset_index()
        cols_to_change = {col : col +'_' + str(qu) for col in num_cols}
        percentiles.rename(columns=cols_to_change, inplace=True)
        if qu == percentile_list[0]:
            all_percentiles = percentiles
        else:
            all_percentiles = pd.merge(all_percentiles, percentiles, how = "left",\
                                       on = non_numeric)
    return all_percentiles

def _drop_correlated(data, score_ordered_cols, max_corr, method='pearson'):
    new = [[score_ordered_cols[0]], [0]]
    corr_matrix = data[score_ordered_cols].corr(method).values
    N = len(score_ordered_cols)
    for i in range(1, N):
        tr = corr_matrix[new[1], i]
        if sum(np.abs(tr) > max_corr) == 0:
            new[0] += [score_ordered_cols[i]]
            new[1] += [i]
    return new[0]


class feature_reduction(BaseEstimator, TransformerMixin):
    def __init__(self, min_mi=.001, max_corr=.7, n_neighbors=11):
        self.min_mi = min_mi
        self.max_corr = max_corr
        self.n_neighbors = n_neighbors

    def fit(self, X:pd.DataFrame, y):
        X = X.copy(deep=True)
        columns = X.columns
        mi = mutual_info_classif(X.values, y, n_neighbors= self.n_neighbors)
        cols_mi = list(zip(columns, mi))
        cols_mi.sort(reverse=True, key=lambda x: x[1])
        cols_mi = [pair[0] for pair in cols_mi if pair[1] > self.min_mi]
        new_cols = _drop_correlated(X[cols_mi], cols_mi, max_corr=self.max_corr)
        self.selected_cols = new_cols
        return self

    def transform(self, X, y=None):
        return X[self.selected_cols]

def cleaning_and_counts(s):
    # Imports/sets here because it'd be executed in subroutine which executes independently from main code
    import ftfy, re, numpy as np
    from string import punctuation, whitespace
    
    # Всі коди дефісу(або аналогічних символів) які я знайшов в текстах
    dashes = [chr(int(d, 16)) for d in ['058A', '05BE', '1400', '1806', '2010', '2011',\
          '2012', '2013', '2014', '2015', '2053', '207B', '208B', '2212', '2E17', \
          '2E1A', '2E3A', '2E3B', '2E40', '2E5D', '301C', '3030', '30A0', 'FE31', \
          'FE32', 'FE58', 'FE63', 'FF0D', '10EAD']]
    dashes_compiled = re.compile('[' + ''.join(dashes) + ']+', flags = re.UNICODE)
    
    s = ftfy.fix_text(s)
    s = re.sub(dashes_compiled, '-', s)     # all dashes should be the same

    url_n = len(re.findall('https?://\\S+\\b', s)) # count urls
    s = re.sub('https?://\\S+\\b', '', s)   # and remove them

    hasht_n = len(re.findall(r'#\w+\b', s)) # count hashtags
    s = re.sub(r'#\w+\b', '', s)            # remove them

    handle_n = len(re.findall(r'@\w{1,15}\b', s)) # count handles
    s = re.sub(r'@\w{1,15}\b', '', s)       # remove them

    s = re.sub('pic\\.twitter\\.com/\\w+\\b', '', s)        # remove pictures. Not expected to impact overall picture
    s = re.sub('\\s+', ' ', s)                              # reducing multiple whitespaces to one
    s = s.lstrip(whitespace + punctuation + '\xa0' + chr(8230))   # removing possible whitespaces in front
    s = s.rstrip(whitespace + '\xa0')         # and on the back
    l=''
    emoj_and_such = 0
    for ch in s:
        if ord(ch) < 8204:
            l += ch             # keep a symbol if not emoji or pictogram or such
        else:
            emoj_and_such += 1  # counting emojis and pictograms
    comma_n = len(re.findall(',', s))
    exl_n =  len(re.findall('!', s))
    dash_n = len(re.findall('-', s))
    a_an_n = len(re.findall(r'\b[Aa]n?\b', s))
    the_n = len(re.findall(r'\b[Tt]he\b', s))

    # reduce a number of repeated symbols to no more than 2 
    l = re.sub(r'(.)\1\1+', r'\1\1', l)
    length = len(l)

    words = [len(w) for w in re.findall(r'\b\w+\b', l)]
    if len(words)==0:
        average_word = 0
    else:
        average_word = np.max(words)
    
    return l, url_n, hasht_n, handle_n, emoj_and_such, exl_n, comma_n, dash_n, a_an_n, the_n, length, average_word



def predict_is_troll(model, data):
    df = pd.DataFrame(data)
    df = df[['account', 'tweet']]

    if df.shape[0] < 10:
        return None

    #df.info()

    # Cleaning
    with mp.Pool(processes= mp.cpu_count()) as p:
        df['tuple'] = p.map(cleaning_and_counts, df.tweet)

    # Memory Optimization
    features = ("cleaned_tweet, url_n, hasht_n, handle_n, emoji_and_such, exl_n, comma_n, dash_n, a_an_n, the_n, length, average_word").split(', ')

    for i in range(len(features)):
        if i ==0:
            df[features[i]] = df.tuple.apply(lambda t: t[i])
        else:
            df[features[i]] = df.tuple.apply(lambda t: t[i]).astype(np.uint8)

    #print(df.columns)
    df.drop(['tuple'], axis=1,inplace=True)
    gc.collect()

    #print(df)

    # Check if total account tweets > 10
    _min_count = 10
    _acc_properties = df[['account']].groupby(['account'])\
        .agg(tweet_count=('account', 'size'))\
        .reset_index()

    #print(_acc_properties)
    _kept_accs = _acc_properties[_acc_properties.tweet_count >= _min_count]
    _restricted = df[df.account.isin(_kept_accs.account)].copy(deep=True)
    #del total_data

    _num_cols = features[1:]
    _restricted.drop(['tweet', 'cleaned_tweet'], axis=1, inplace=True)
    #print("Restricted")
    #_restricted


    # Generate features
    _all_percentiles = percentile_calc(_restricted[['account']+_num_cols], \
                                    groupby_col='account', num_cols=_num_cols,
                                    percentile_list=range(10, 100, 10))
        
    #_new_features = _all_percentiles.columns[2:]
    #print(_all_percentiles)

    preditction = model.predict(_all_percentiles)[0]
    prediction_proba = model.predict_proba(_all_percentiles)[0]

    #print(f"Proba: {prediction_proba}")


    #print("\nPrediction: " + ("Troll Detected" if preditction == 1 else "Regular User"))
    #print("Troll Account Probability: " + str(prediction_proba[1]))



    return preditction == 1, round(prediction_proba[1], 4)
