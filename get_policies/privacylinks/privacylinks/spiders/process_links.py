import pandas as pd

'''
df_comp = pd.read_csv('/home/user/Scrapy/privacylinks/data/second/2019-08-15T23-53-34.csv')
df1 = pd.read_csv('/home/user/Scrapy/privacylinks/data/second/2019-08-16T02-18-06.csv')
df2 = pd.read_csv('/home/user/Scrapy/privacylinks/data/second/2019-08-16T06-40-45.csv')

good_comp = df_comp.url[df_comp.fail.isna()] #2416 vs 10781
good_df1 = df1.url[df1.fail.isna()] #7994 vs 43716
good_df2 = df2.url[df2.fail.isna()]#9846 vs 57474

no_priv_comp = df_comp.url[df_comp.fail == 'NO PRIVACY IN BODY']
no_priv_df1 = df1.url[df1.fail == 'NO PRIVACY IN BODY']
no_priv_df2 = df2.url[df2.fail == 'NO PRIVACY IN BODY']

#no_priv_comp.to_csv('/home/user/Scrapy/privacylinks/data/second/no_priv_comp.csv', index=False)
#no_priv_df1.to_csv('/home/user/Scrapy/privacylinks/data/second/no_priv_df1.csv', index=False)
#no_priv_df2.to_csv('/home/user/Scrapy/privacylinks/data/second/no_priv_df2.csv', index=False)
#good_comp.to_csv('/home/user/Scrapy/privacy-policy-files/comp_ready_first_crawl.csv', index=False)
#good_df1.to_csv('/home/user/Scrapy/privacy-policy-files/df1_ready_first_crawl.csv', index=False)
#good_df2.to_csv('/home/user/Scrapy/privacy-policy-files/df2_ready_first_crawl.csv', index=False)
'''

df_comp = pd.read_csv('/home/user/Scrapy/privacy-policy-files/comp_privacy_links/comp_good_privacy_second_crawl.csv')
df1 = pd.read_csv('/home/user/Scrapy/privacy-policy-files/df1_privacy_links/df1_good_privacy_second_crawl.csv')
df2 = pd.read_csv('/home/user/Scrapy/privacy-policy-files/df2_privacy_links/df2_good_second_crawl.csv')

good_comp = df_comp.url[df_comp.fail.isna()] #2416 vs 10781
good_df1 = df1.url[df1.fail.isna()] #7994 vs 43716
good_df2 = df2.url[df2.fail.isna()]#9846 vs 57474

good_comp.to_csv('/home/user/Scrapy/privacy-policy-files/comp_ready_second_crawl.csv', index=False)
good_df1.to_csv('/home/user/Scrapy/privacy-policy-files/df1_ready_second_crawl.csv', index=False)