import pandas as pd

df = pd.read_csv('/home/user/Scrapy/df1_ready_merged.csv', names=['urls'])
df = df[~df.duplicated()] #7159
privacy = df[df.urls.str.contains('privacy')] #4347
terms = df[df.urls.str.contains('terms')] # 1917
rest = df[(~df.urls.str.contains('privacy')) & (~df.urls.str.contains('terms'))] #965
