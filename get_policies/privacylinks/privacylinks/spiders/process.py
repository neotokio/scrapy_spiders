import pandas as pd

'''
df1 = pd.read_csv('/home/user/Scrapy/privacylinks/data/second/2019-08-15T23-14-37.csv') #Short version - check for privacy only
df2 = pd.read_csv('/home/user/Scrapy/privacylinks/data/second/2019-08-15T23-53-34.csv') #Long version computers (to merge!) - check for privacy/terms/legal

len(df1[df1.fail.str.contains('NO PRIVACY IN BODY') == True]) #4213 Marked as NO PRIVACY
len(df2[df2.fail.str.contains('NO PRIVACY IN BODY') == True]) #7736
len(df1[df1.fail.str.contains('TIMEOUT') == True]) #773
len(df2[df2.fail.str.contains('TIMEOUT') == True]) #629


df1 = pd.read_csv('/home/user/Scrapy/privacylinks/privacylinks/spiders/AlexaPart1_processed.csv', index_col=None)
df2 = pd.read_csv('/home/user/Scrapy/privacylinks/privacylinks/spiders/AlexaPart2_processed.csv', index_col=None)

full = df1.append(df2)
'''

comp = pd.read_csv('/home/user/Scrapy/privacy-policy-files/comp_privacy_links/comp_ready_merged.csv')