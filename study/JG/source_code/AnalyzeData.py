import pandas as pd
import matplotlib.pyplot as plt
import nltk
import seaborn as sns
from collections import defaultdict
from plotly import tools
import plotly.offline as py
from datetime import datetime
import time
from nltk.tokenize import word_tokenize
from nltk import ngrams
from NGram import NGram
from collections import Counter

'''
변경 사항, 따로 언급이 없는 이상
모든 데이터 분석은 전체 데이터(training data + test data)에 대해 수행됨

'''
df_train = pd.read_csv("../../../dataset/drugsComTrain_raw.csv", parse_dates=["date"], infer_datetime_format=True)
df_test = pd.read_csv("../../../dataset/drugsComTest_raw.csv", parse_dates=["date"], infer_datetime_format=True)

plt.figure(0)
wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
colors = ['#8fd9b6', '#ff9999']
plt.pie([len(df_train), len(df_test)], labels=["Training data", "Test data"],wedgeprops=wedgeprops, colors=colors, startangle=260, shadow=False, autopct='%.1f%%', textprops={'fontsize':16})
plt.title("Percentage of Data", fontsize=18)

plt.savefig("percentageofData.png")

print('training data 에서 attribute 목록: ', df_train.columns.tolist())
print('test data 에서 attribute 목록: ', df_test.columns.tolist())

pd.set_option('display.max_columns', 7)
print(df_train.head())

df_all = pd.concat([df_train, df_test]).reset_index()
del df_all['index']

print(df_all['review'].head(5))
'''
#uniqueID 분석 시작
'''

uniqueValue = df_all.shape[0]
print("uniqueID를 기준으로 중복된 데이터 있는지 확인 : ", uniqueValue)
print("set 메서드를 이용해서 중복 개수 확인 : ", len(set(df_all['uniqueID'].values)))

print("The number of unique condition is ", len(set(df_all['condition'])))
print("The number of unique drugName is ", len(set(df_all['drugName'])))

'''
#drugName과 condition분석 시작
'''

plt.figure(1)
condition_dn = df_all.groupby(['condition'])['drugName'].nunique().sort_values(ascending=False)
colors = sns.color_palette('hls',20)
plot1 = condition_dn[0:20].plot(kind="bar", figsize = (14,17), fontsize = 10,color=colors)
for p in plot1.patches:
    left, bottom, width, height = p.get_bbox().bounds
    plot1.annotate("%d" % height, (left+width/2, height*1.01), ha='center')
plot1.text(10, 120, "This x label (this comment is helpful)\n is wrong due to crawling process ", fontsize=18, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
plot1.annotate('', xy=(15, 64), xytext=(16, 115), arrowprops=dict(facecolor='black', shrink=0.05))
plot1.annotate('', xy=(19, 59), xytext=(17, 115), arrowprops=dict(facecolor='black', shrink=0.05))
plt.xlabel("", fontsize = 17)
plt.ylabel("The number of drugs", fontsize = 15)
plt.title("Top20 : The number of drugs per condition.", fontsize = 20)
plt.plot()
plt.savefig('./number_of_drugs_per_condition.png')

plt.figure(2)
condition_dn[condition_dn.shape[0]-20:condition_dn.shape[0]].plot(kind="bar", figsize = (14,10), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("The number of drugs", fontsize = 15)
plt.title("Bottom20 : The number of drugs per condition.", fontsize = 20)
plt.plot()
plt.savefig('./number_of_drugs_per_condition_bottom20.png')

plt.figure(3)
drugName_dn = df_all.groupby(['drugName'])['condition'].nunique().sort_values(ascending=False)
plot1 = drugName_dn[0:20].plot(kind="bar", figsize = (14,17), fontsize = 10,color=colors)
for p in plot1.patches:
    left, bottom, width, height = p.get_bbox().bounds
    plot1.annotate("%d" % height, (left+width/2, height*1.01), ha='center')
plt.xlabel("", fontsize = 20)
plt.ylabel("The number of conditions", fontsize = 15)
plt.title("Top20 : The number of condition per drug.", fontsize = 20)
plt.plot()
plt.savefig('./number_of_condition_per_drug.png')

plt.figure(4)
plot1 = drugName_dn[drugName_dn.shape[0]-20:drugName_dn.shape[0]].plot(kind="bar", figsize = (14,10), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("The number of conditions", fontsize = 15)
plot1.text(15.71, 0.1, '0 count is due to missing \nvalue for some condtions', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

plot1.annotate('', xy=(16, 0), xytext=(16, 0.07), arrowprops=dict(facecolor='black', shrink=0.05))
plot1.annotate('', xy=(17, 0), xytext=(17, 0.07), arrowprops=dict(facecolor='black', shrink=0.05))
plot1.annotate('', xy=(18, 0), xytext=(18, 0.07), arrowprops=dict(facecolor='black', shrink=0.05))
plot1.annotate('', xy=(19, 0), xytext=(19, 0.07), arrowprops=dict(facecolor='black', shrink=0.05))
plt.title("Bottom20 : The number of condition per drug.", fontsize = 20)
plt.plot()
plt.savefig('./number_of_condition_per_drug_bottom20.png')

'''
#rating 분석 시작
'''

rating = df_all['rating'].value_counts().sort_values(ascending=False)
plt.figure(5)
plot1 = rating[:].plot(kind="bar", figsize = (14,6), fontsize = 10,color=colors)
for p in plot1.patches:
    left, bottom, width, height = p.get_bbox().bounds
    plot1.annotate("%d" % height, (left+width/2, height*1.01), ha='center')
plt.xlabel("Rating", fontsize = 12)
plt.ylabel("The number of reviews", fontsize = 12)
plt.title("Count of rating values", fontsize = 20)
plt.plot()
plt.savefig('./count_of_rating_values')


rating_ratio = df_all['rating'].value_counts() / df_all['rating'].count()
plt.figure(6, figsize=(8, 8))
plt.title("Ratio of counts", fontsize=20)
explode = []
for i in range(0, 10):
    explode.append(float(0.01))
plot1 = plt.pie(rating_ratio, labels=rating_ratio.index, autopct='%1.f%%', startangle=90, explode=explode, textprops={'fontsize':16})
plt.savefig('./ratio_of_rating')

plt.figure(7, figsize=(8,8))
plt.xlabel('Rating')
plt.ylabel('Dist')
plt.title("Distribution of rating", fontsize=20)
sns.distplot(df_all['rating'], hist=False)
plt.savefig('./distribution_of_rating.png')

print("가장 처음 날짜 : ", df_all['date'].min())
print("가장 마지막 날짜 : ",  df_all['date'].max())

cnt_srs = df_all['date'].dt.year.value_counts()
cnt_srs = cnt_srs.sort_index()
plt.figure(8)
plot1 = cnt_srs[:].plot(kind="bar", figsize = (14,6), fontsize = 10,color=colors)
for p in plot1.patches:
    left, bottom, width, height = p.get_bbox().bounds
    plot1.annotate("%d" % height, (left+width/2, height*1.01), ha='center')
firstreview = df_all['date'].min().strftime('%Y-%m-%d')
lastreview = df_all['date'].max().strftime('%Y-%m-%d')
plot1.text(0.2, 25000, "First review is written at " + firstreview + "\nAnd recent review is written at " + lastreview, fontsize=20, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
plt.xlabel('year', fontsize=12)
plt.ylabel('The number of reviews', fontsize=12)
plt.title("Number of reviews in year")
plt.plot()
plt.savefig('./Number_of_reviews_in_year.png')

plt.figure(9)
df_all['month'] = pd.to_datetime(df_all['date'], errors='coerce')
cnt = df_all['month'].dt.month.value_counts()
cnt = cnt.sort_index()
plt.figure(figsize=(9,6))
sns.barplot(cnt.index, cnt.values,color='blue',alpha=0.4)
plt.xticks(rotation='vertical')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title("Reviews per month")
plt.savefig('./Reviews_per_month.png')

plt.figure(10)
df_all['day'] = pd.to_datetime(df_all['date'], errors='coerce')
cnt = df_all['day'].dt.day.value_counts()
cnt = cnt.sort_index()
plt.figure(figsize=(9,6))
sns.barplot(cnt.index, cnt.values,color='blue',alpha=0.4)
plt.xticks(rotation='vertical')
plt.xlabel('Day', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title("Reviews per day")
plt.savefig('./Review_per_day.png')

df_day = pd.DataFrame.copy(df_all)
df_day['day'] = df_day['date'].dt.day
rating = df_day.groupby('day')['rating'].mean()
plt.figure(11)
rating.plot(kind="bar", figsize= (14, 6), fontsize=10, color="green")
plt.xlabel('year', fontsize=12)
plt.ylabel('Mean rating', fontsize=12)
plt.title("Mean rating in day", fontsize=12)
plt.plot()
plt.savefig('./Mean_rating_in_day.png')

plt.figure(12)
plot1 = sns.distplot(df_all['usefulCount'].dropna(), color="green")
plt.xticks(rotation='vertical')
plt.xlabel('', fontsize=12)
plt.ylabel('', fontsize=12)
plt.title("Distribution of usefulCount")
description = df_all['usefulCount'].describe()
plot1.text(200, 0.012, str(description), fontsize=15, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
plt.plot()
plt.savefig('./Distribution_of_usefulCount.png')


print('usefulCount의 대한 통계', df_all['usefulCount'].describe())
'''
df_ = df_all[['rating', 'review']]
df_['review'] = df_['review'].str.replace("&#039;", "")
df_['review'] = df_['review'].str.replace(r'[^\w\d\s]',' ')

df_review_5 = " ".join(df_.loc[df_.rating <= 5, 'review'])
df_review_10 = " ".join(df_.loc[df_.rating > 5, 'review'])

token_review_5 = word_tokenize(df_review_5)
token_review_10 = word_tokenize(df_review_10)

unigrams_5 = ngrams(token_review_5, 1)
unigrams_10 = ngrams(token_review_10, 1)

frequency_5 = Counter(unigrams_5)
frequency_10 = Counter(unigrams_10)

df_5 = pd.DataFrame(frequency_5.most_common(20))
df_10 = pd.DataFrame(frequency_10.most_common(20))

# 차트
plt.figure(13, figsize=(30, 25))
fig, ax = plt.subplots(1,2)
sns.set(font_scale = 1, style = 'whitegrid')
sns_5 = sns.barplot(x = df_5[1], y = df_5[0], color = 'lightsteelblue', ax = ax[0])
sns_10 = sns.barplot(x = df_10[1], y = df_10[0], color = 'lightsteelblue', ax = ax[1])

# 축 설정
sns_5.set_title("Top 20 unigrams according for rating <= 5", fontsize=7)
sns_10.set_title("Top 20 unigrams according for rating > 5", fontsize=7)
sns_5.set_ylabel("Unigrams");
'''


#review에 대한 N-gram 분석 시작
'''
'''
df_all_6_10 = df_all[df_all["rating"]>5]
df_all_1_5 = df_all[df_all["rating"]<6]

ngram = NGram()

freq_dict = defaultdict(int)
for sent in df_all_1_5["review"]:
    for word in ngram.generate_ngrams(sent):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace0 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'blue')

## Get the bar chart from rating  4 to 7 review ##
freq_dict = defaultdict(int)
for sent in df_all_6_10["review"]:
    for word in ngram.generate_ngrams(sent):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace1 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'blue')

# Creating two subplots
fig = tools.make_subplots(rows=1, cols=2, vertical_spacing=0.04,
                          subplot_titles=["Frequent words of rating 1 to 5",
                                          "Frequent words of rating 6 to 10"])
fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig['layout'].update(height=1200, width=900, paper_bgcolor='rgb(233,233,233)', title="Word Count Plots")
py.iplot(fig, filename='word-plots')

freq_dict = defaultdict(int)
for sent in df_all_1_5["review"]:
    for word in ngram.generate_ngrams(sent,2):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace1 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'orange')

freq_dict = defaultdict(int)
for sent in df_all_6_10["review"]:
    for word in ngram.generate_ngrams(sent,2):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace2 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'orange')

# Creating two subplots
fig = tools.make_subplots(rows=1, cols=2, vertical_spacing=0.04,horizontal_spacing=0.15,
                          subplot_titles=["Frequent biagrams of rating 1 to 5",
                                          "Frequent biagrams of rating 6 to 10"])
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig['layout'].update(height=1200, width=1000, paper_bgcolor='rgb(233,233,233)', title="Bigram Count Plots")
py.iplot(fig, filename='word-plots')

freq_dict = defaultdict(int)
for sent in df_all_1_5["review"]:
    for word in ngram.generate_ngrams(sent,3):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace1 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'green')

freq_dict = defaultdict(int)
for sent in df_all_6_10["review"]:
    for word in ngram.generate_ngrams(sent,3):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace2 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'green')

# Creating two subplots
fig = tools.make_subplots(rows=1, cols=2, vertical_spacing=0.04,horizontal_spacing=0.15,
                          subplot_titles=["Frequent trigrams of rating 1 to 5",
                                          "Frequent trigrams of rating 6 to 10"])
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig['layout'].update(height=1200, width=1600, paper_bgcolor='rgb(233,233,233)', title="Trigram Count Plots")
py.iplot(fig, filename='word-plots')

freq_dict = defaultdict(int)
for sent in df_all_1_5["review"]:
    for word in ngram.generate_ngrams(sent,4):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace1 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'red')

freq_dict = defaultdict(int)
for sent in df_all_6_10["review"]:
    for word in ngram.generate_ngrams(sent,4):
        freq_dict[word] += 1
fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
fd_sorted.columns = ["word", "wordcount"]
trace2 = ngram.horizontal_bar_chart(fd_sorted.head(50), 'red')

# Creating two subplots
fig = tools.make_subplots(rows=1, cols=2, vertical_spacing=0.04,horizontal_spacing=0.15,
                          subplot_titles=["Frequent 4-grams of rating 1 to 5",
                                          "Frequent 4-grams of rating 6 to 10"])
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig['layout'].update(height=1200, width=1600, paper_bgcolor='rgb(233,233,233)', title="4-grams Count Plots")
py.iplot(fig, filename='word-plots')

plt.show()