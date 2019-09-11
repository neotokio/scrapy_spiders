from svd_processing import privacy_css, privacy_only
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

def css():
    priv_css_token = [word_tokenize(i) for i in privacy_css['privacy']]
    css_flat = []

    for word in priv_css_token:
        for item in word:
            css_flat.append(item)
    return css_flat


css_list = css()


def non_css():
    priv_slice = privacy_only['privacy']
    priv_token = [word_tokenize(i) for i in priv_slice]
    priv_flat = []

    for words in priv_token:
        for item in words:
            priv_flat.append(item)
    return priv_flat


priv_list = non_css()

count = Counter(priv_list)
top50 = count.most_common(50)

count2 = Counter(css_list)
top50_2 = count2.most_common(50)
del top50[0:2]
del top50_2[0:2]

plot_df = pd.DataFrame(top50, columns=['words', 'freq'])
plot_df2 = pd.DataFrame(top50_2, columns=['words', 'freq'])

#STACKED GROUPED BAR CHART
barWidth = 0.3
matplotlib.rc('xtick', labelsize=8)
plt.bar(x=plot_df['words'], height=plot_df['freq'], width=barWidth, label='NonCSS Policies')
plt.bar(x=plot_df2['words'], height=plot_df2['freq'], width=barWidth, label='CSS Policies')
plt.xticks(rotation='vertical')
plt.legend()
plt.show()

#Find most occuring words in first 100 strings
first_100 = privacy_css.apply(lambda x: x.str.split().str[0:100])
first_100 = first_100['privacy']
css_flat = []

for word in first_100:
    for item in word:
        css_flat.append(item)
