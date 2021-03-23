import pandas as pd
import matplotlib.pyplot as plt
import nltk
import seaborn as sns
from collections import defaultdict
from plotly import tools
import plotly.offline as py

from NGram import NGram

df_train = pd.read_csv("drugsComTrain_raw.csv", parse_dates=["date"], infer_datetime_format=True)
df_test = pd.read_csv("drugsComTest_raw.csv", parse_dates=["date"], infer_datetime_format=True)

plt.figure(0)
wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
plt.pie([len(df_train), len(df_test)], labels=["training data", "test data"],wedgeprops=wedgeprops, startangle=200, shadow=True, autopct='%.1f%%')
plt.title("Percentage of Data")
plt.savefig("percentageofData.png")

print('training data 에서 attribute : ', df_train.columns)
print('test data 에서 attribute : ', df_test.columns)

pd.set_option('display.max_columns', 7)
print(df_train.head())

df_all = pd.concat([df_train, df_test]).reset_index()
del df_all['index']

'''uniqueID 분석 시작'''

uniqueValue = df_all.shape[0]
print("uniqueID를 기준으로 중복된 데이터 있는지 확인 : ", uniqueValue)
print("set 메서드를 이용해서 중복 개수 확인 : ", len(set(df_all['uniqueID'].values)))

print("The number of unique condition is ", len(set(df_all['condition'])))
print("The number of unique drugName is ", len(set(df_all['drugName'])))

'''drugName과 condition분석 시작'''

plt.figure(1)
condition_dn = df_all.groupby(['condition'])['drugName'].nunique().sort_values(ascending=False)
condition_dn[0:20].plot(kind="bar", figsize = (14,6), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Top20 : The number of drugs per condition.", fontsize = 20)
plt.plot()
plt.savefig('./number of drugs per condition.png')

plt.figure(2)
condition_dn[condition_dn.shape[0]-20:condition_dn.shape[0]].plot(kind="bar", figsize = (14,6), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Bottom20 : The number of drugs per condition.", fontsize = 20)
plt.plot()
plt.savefig('./number of drugs per condition bottom20.png')

plt.figure(3)
drugName_dn = df_all.groupby(['drugName'])['condition'].nunique().sort_values(ascending=False)
drugName_dn[0:20].plot(kind="bar", figsize = (14,6), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Top20 : The number of condition per drug.", fontsize = 20)
plt.plot()
plt.savefig('./number of condition per drug.png')

plt.figure(4)
drugName_dn[drugName_dn.shape[0]-20:drugName_dn.shape[0]].plot(kind="bar", figsize = (14,6), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Bottom20 : The number of condition per drug.", fontsize = 20)
plt.plot()
plt.savefig('./number of condition per drug bottom20.png')

'''rating 분석 시작'''

rating = df_all['rating'].value_counts().sort_values(ascending=False)
plt.figure(5)
rating[:].plot(kind="bar", figsize = (14,6), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Count of rating values", fontsize = 20)
plt.plot()
plt.savefig('./count of rating values')

print("가장 처음 날짜 : ", df_all['date'].min())
print("가장 마지막 날짜 : ", df_all['date'].max())

cnt_srs = df_all['date'].dt.year.value_counts()
cnt_srs = cnt_srs.sort_index()
plt.figure(6)
cnt_srs[:].plot(kind="bar", figsize = (14,6), fontsize = 10,color="green")
plt.xlabel('year', fontsize=12)
plt.ylabel('', fontsize=12)
plt.title("Number of reviews in year")
plt.plot()
plt.savefig('./Number of reviews in year.png')

df_day = pd.DataFrame.copy(df_all)
df_day['day'] = df_day['date'].dt.day
print("크기", df_day.shape)
rating = df_day.groupby('day')['rating'].mean()
plt.figure(7)
rating.plot(kind="bar", figsize= (14, 6), fontsize=10, color="green")
plt.xlabel('year', fontsize=12)
plt.ylabel('', fontsize=12)
plt.title("Mean rating in day", fontsize=12)
plt.plot()
plt.savefig('./Mean rating in day.png')

plt.figure(8)
sns.distplot(df_all['usefulCount'].dropna(), color="green")
plt.xticks(rotation='vertical')
plt.xlabel('', fontsize=12)
plt.ylabel('', fontsize=12)
plt.title("Distribution of usefulCount")
plt.plot()
plt.savefig('./Distribution of usefulCount.png')

print('usefulCount의 대한 통계', df_all['usefulCount'].describe())

'''
review에 대한 N-gram 분석 시작
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