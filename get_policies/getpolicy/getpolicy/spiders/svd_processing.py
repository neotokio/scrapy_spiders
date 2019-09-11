import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import time
from nltk.tokenize import word_tokenize
from collections import Counter
from sklearn import decomposition
from scipy import linalg
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer


np.set_printoptions(suppress=True)
engine = create_engine('postgresql://gp_user:test1@localhost:5432/gp_db')
df = pd.read_sql_query('SELECT * FROM scraped', engine)
df.drop(['id'], axis=1, inplace=True)
privacy_only = df[~df.privacy.isna()]


privacy_css = privacy_only[privacy_only['privacy'].str.contains('inline|font|img|margin|px|padding|menu')]
privacy_only = privacy_only[~privacy_only['privacy'].str.contains('inline|font|img|margin|px|padding|menu')]
privacy_only = privacy_only[privacy_only['privacy'].str.len() > 1000]
privacy_css = privacy_css[privacy_css['privacy'].str.len() > 1000]

start = time.time()

'''CLEAN DOCUMENTS FROM UNNECESSARY NOISE'''
REPLACE1= re.compile('[/(){}\[\]\|@,;]') # Remove special signs
BAD_1 = re.compile('[^0-9A-Za-z #+_,.]') # Remove everything which is NOT [] - add ., if You want to keep punctuation
HASH_REMOVE = re.compile('#\S+') # Remove any word with hash in front
DIGIT_REMOVE = re.compile('\d\w*') # Remove any word with digit
FIRST_CSS = re.compile('[\#\.\w\-\,\s\n\r\t:]+(?=\s*\{)')
CSS_TAG2 = re.compile('.*;')
JS_RM = re.compile('/\**.*\/')
SPACES = re.compile('\s\s+')
STOPWORDS = set(stopwords.words('english')) # Remove stopwords
#FIRST_CSS = re.compile('[@.#a-zA-Z][^}]*?(?={)')
#CSS_TAG = re.compile('{.+}') # Remove anything within {}


def clean_css(text):
    text = BeautifulSoup(text, "lxml").text
    text = CSS_TAG2.sub(' ', text)
    text = FIRST_CSS.sub(' ', text)
    text = JS_RM.sub(' ', text)
    text = HASH_REMOVE.sub(' ', text)
    text = DIGIT_REMOVE.sub(' ', text)
    text = BAD_1.sub(' ', text)
    text = SPACES.sub(' ', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text


privacy_css['privacy'] = privacy_css['privacy'].apply(clean_css)
privacy_css = privacy_css[privacy_css['privacy'].str.len() > 1000]
end = time.time()
print(end - start)
print('NOW NONCSS')
start = time.time()


def clean_noncss(text):
    text = BeautifulSoup(text, "lxml").text
    text = CSS_TAG2.sub(' ', text)
    text = FIRST_CSS.sub(' ', text)
    text = BAD_1.sub(' ', text)
    text = SPACES.sub(' ', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text


privacy_only['privacy'] = privacy_only['privacy'].apply(clean_noncss)
privacy_only = privacy_only[privacy_only['privacy'].str.len() > 1000]
end = time.time()
print(end - start)



privacy_df = pd.concat([privacy_css, privacy_only])

''' TOKENIZE EACH COLUMN
privacy_df['tokenized'] = privacy_df.apply(lambda row: word_tokenize(row['privacy']), axis=1)

STORE DATA BACK INTO DB
engine = create_engine('postgresql://p_db:testpass1@localhost:5432/privacy_process')
con = engine.connect()
table_name = 'privacy_processed'
privacy_df.to_sql(table_name, con)
con.close()

PRINT COUNT
priv_slice = privacy_only['privacy']
priv_token = [word_tokenize(i) for i in priv_slice]
priv_flat = []

for words in priv_token:
    for item in words:
        priv_flat.append(item)

count = Counter(priv_flat)
top50 = count.most_common(50)
#plot_df = pd.DataFrame(top50, columns=['words', 'freq'])
#plot_df.plot(kind='barh', x='words')
'''















'''
# plot_df = pd.DataFrame(top40, columns=['words', 'freq'])
# plot_df.plot(kind='barh', x='words')

#count = Counter(css_list)
#count_list = count.most_common(50)

#Check lenght of string in column
for lenght in privacy_only['privacy']:
    lenght = sum(len(lenght) for lenght in privacy_only['privacy']) 
    

#REMOVE IN COLUMN FROM LIST
p = re.compile('|'.join(map(re.escape, to_remove)))
privacy_css['privacy'] = [p.sub('', text) for text in privacy_css['privacy']]
to_remove = ['icon', 'ul', 'webkit', 'fusion', 'menu', 'hover', 'header', '.mega', 'none', 'color', 'width', 'img wp', 'img emoji',
             'block', 'background', 'margin', 'font', 'display', 'padding', 'border', 'height', 'box',
             'align', 'inline', 'size', 'shadow', 'vertical', 'smiley', 'li', 'bottom', 'important']

# WE SHOULD ADD REGEX/DICTIONARY TO REMOVE ALL NON WORDS (CSS TAGS)
#privacy_only['privacy'][0:1].str.get_dummies(sep=' ').sum() --- THIS WILL EXTRACT MOST COMMON WORDS ASSUMPTIONS IS THAT THEY WILL BE REPEATED BECAUSE CSS USES THE SAME WORDS
1. Iterate through each policy and print 10 most common words (exclude stopwords accordingly)
2. Make TDF-IF and SVD topic modelling for 6000 documents (start with 10....)
    * Extract most common features from this models
3. Compare to distinvtive TOSDR keys
'''
