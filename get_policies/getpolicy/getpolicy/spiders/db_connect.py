import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner


engine = create_engine('postgresql://gp_user:test1@localhost:5432/gp_db')
df = pd.read_sql_query('SELECT * FROM scraped', engine)
df.drop(['id'], axis=1, inplace=True)
privacy = df.privacy[~df.privacy.isna()]
terms = df.terms[~df.terms.isna()]
without_docs = df[(df.privacy.isna()) & (df.terms.isna())]

new_df = df[['privacy', 'terms', 'domain']]

#df['privacy'] = df['privacy'].apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
#privacy.apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())

df.privacy.drop_duplicates(inplace=True)
df.terms.drop_duplicates(inplace=True)

#new_df = df[['privacy', 'terms', 'domain']]
#new_df.loc[new_df['privacy'] == 'None', 'privacy'] = 'text'

