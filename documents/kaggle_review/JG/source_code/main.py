import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from sklearn import model_selection, preprocessing, metrics, ensemble, naive_bayes, linear_model
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
import lightgbm as lgb

from bs4 import BeautifulSoup
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split
from sklearn import metrics

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, Conv1D
from tensorflow.python.keras.layers import CuDNNGRU
from tensorflow.keras.layers import Bidirectional, GlobalMaxPool1D
from tensorflow.keras.models import Model
from tensorflow.keras import initializers, regularizers, constraints, optimizers, layers
import tensorflow.python.keras as keras

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Bidirectional, LSTM, BatchNormalization, Dropout
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

import numpy as np
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import random
import os

from sklearn.metrics import roc_auc_score, precision_recall_curve, roc_curve, average_precision_score
from sklearn.model_selection import KFold
from lightgbm import LGBMClassifier
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import load_model

pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999

'''
raw_data = pd.DataFrame(columns=['review'])
raw_data = input("type your condition or symptom : ")
raw_data_frame = pd.DataFrame(columns=['review'])
test = raw_data_frame.append({'review' : raw_data}, ignore_index=True)
print(test['review'])
'''

df_train = pd.read_csv("../../../dataset/drugsComTrain_raw.csv", parse_dates=["date"], infer_datetime_format=True)
df_test = pd.read_csv("../../../dataset/drugsComTest_raw.csv", parse_dates=["date"], infer_datetime_format=True)


os.environ["CUDA_VISIBLE_DEVICES"] = "1"

print("Train shape :", df_train.shape)
print("Test shape :", df_test.shape)

# data set has 7 attributes
'''
pd.set_option('display.max_columns', 7)
print(df_train.head())

df_all = pd.concat([df_train, df_test]).reset_index()
del df_all['index']

plt.figure(0)
condition_dn = df_all.groupby(['condition'])['drugName'].nunique().sort_values(ascending=False)
condition_dn[0:20].plot(kind="bar", figsize = (14,6), fontsize = 10,color="green")
plt.xlabel("", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Top20 : The number of drugs per condition.", fontsize = 20)
plt.plot()
plt.savefig('./number of drugs per condition.png')

percent = (df_all.isnull().sum()).sort_values(ascending=False)
plt.figure(1)
percent.plot(kind="bar", figsize = (14,6), fontsize = 10, color='green')
plt.xlabel("Columns", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Total Missing Value ", fontsize = 20)
plt.plot()
plt.savefig('./total missing value.png')

print("Missing value (%):", 1200/df_all.shape[0] *100)
'''
'''
Data Preprocessing - delete missing value
'''

df_train = df_train.dropna(axis=0)
df_test = df_test.dropna(axis=0)
df_all = pd.concat([df_train, df_test]).reset_index()
#concat data
'''
percent = (df_all.isnull().sum()).sort_values(ascending=False)
plt.figure(2)
percent.plot(kind="bar", figsize = (14,6), fontsize = 10, color='green')
plt.xlabel("Columns", fontsize = 20)
plt.ylabel("", fontsize = 20)
plt.title("Total Missing Value ", fontsize = 20)
plt.plot()
plt.savefig('./total missing value after preprocessing.png')
plt.show()
'''
'''
Data Preprocessing - delete '</span>' phrase in data by crawling data set
'''
all_list = set(df_all.index)
span_list = []

for i, j in enumerate(df_all['condition']):
    if '</span>' in j:
        span_list.append(i)

new_idx = all_list.difference(set(span_list))
df_all = df_all.iloc[list(new_idx)].reset_index()
del df_all['index']

df_condition = df_all.groupby(['condition'])['drugName'].nunique().sort_values(ascending=False)
df_condition = pd.DataFrame(df_condition).reset_index()
df_condition.tail(20)

df_condition_1 = df_condition[df_condition['drugName']==1].reset_index()
df_condition_1['condition'][0:10]

all_list = set(df_all.index)
condition_list = []
for i, j in enumerate(df_all['condition']):
    for c in list(df_condition_1['condition']):
        if j == c:
            condition_list.append(i)

all_list = set(df_all.index)
condition_list = []
for i, j in enumerate(df_all['condition']):
    for c in list(df_condition_1['condition']):
        if j == c:
            condition_list.append(i)

new_idx = all_list.difference(set(condition_list))
df_all = df_all.iloc[list(new_idx)].reset_index()
del df_all['index']
# delete conditions with only one drug

'''
Review Preprocessing
'''

stops = set(stopwords.words('english'))

not_stop = ["aren't","couldn't","didn't","doesn't","don't","hadn't","hasn't","haven't","isn't","mightn't","mustn't","needn't","no","nor","not","shan't","shouldn't","wasn't","weren't","wouldn't"]
for i in not_stop:
    stops.remove(i)

stemmer = SnowballStemmer('english')


def review_to_words(raw_review):
    # 1. Delete HTML
    review_text = BeautifulSoup(raw_review, 'html.parser').get_text()
    # 2. Make a space
    letters_only = nltk.re.sub('[^a-zA-Z]', ' ', review_text)
    # 3. lower letters
    words = letters_only.lower().split()
    # 5. Stopwords
    meaningful_words = [w for w in words if not w in stops]
    # 6. Stemming
    stemming_words = [stemmer.stem(w) for w in meaningful_words]
    # 7. space join words
    return( ' '.join(stemming_words))

df_all['review_clean'] = df_all['review'].apply(review_to_words)


def plot_wordcloud(text, mask=None, max_words=200, max_font_size=100, figure_size=(24.0, 16.0),
                   title=None, title_size=40, image_color=False):
    plt.figure(3)
    stopwords = set(STOPWORDS)
    more_stopwords = {'one', 'br', 'Po', 'th', 'sayi', 'fo', 'Unknown'}
    stopwords = stopwords.union(more_stopwords)

    wordcloud = WordCloud(background_color='white',
                          stopwords=stopwords,
                          max_words=max_words,
                          max_font_size=max_font_size,
                          random_state=42,
                          width=800,
                          height=400,
                          mask=mask)
    wordcloud.generate(str(text))

    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask);
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear");
        plt.title(title, fontdict={'size': title_size,
                                   'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud);
        plt.title(title, fontdict={'size': title_size, 'color': 'black',
                                   'verticalalignment': 'bottom'})
    plt.axis('off');
    plt.tight_layout()
    plt.savefig('world cloud of stops.png')
    plt.show()



#plot_wordcloud(stops, title="World Cloud of stops")



'''
Start making model

Deep Learning Model Using N-gram
'''

df_all['sentiment'] = df_all["rating"].apply(lambda x: 1 if x > 5 else 0)

print("[my]df_all analyze : ")
print(df_all)


df_train, df_test = train_test_split(df_all, test_size=0.33, random_state=42)

vectorizer = CountVectorizer(analyzer = 'word',
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             min_df = 2, # 토큰이 나타날 최소 문서 개수
                             ngram_range=(4, 4),
                             max_features = 20000
                            )
# parameter description

'''
ngram_range(4, 4) : 단어장 생성에 사용할 토큰의 크기를 4로 정함
min_df = 2 : 문서에서 토큰이 나타난 횟수가 2미만일 경우 무시(단어장에 포함되기 위한 최소 빈도)
    
 
'''

pipeline = Pipeline([
    ('vect', vectorizer),
])

train_data_features = pipeline.fit_transform(df_train['review_clean'])
test_data_features = pipeline.fit_transform(df_test['review_clean'])

print("데이터 확인")
print(train_data_features)

# 1. Dataset
y_train = df_train['sentiment']
y_test = df_test['sentiment']
solution = y_test.copy()

print("[my] y_train : ")
print(y_train)

# 2. Model Structures
'''
model = tensorflow.keras.models.Sequential()

model.add(keras.layers.Dense(200, input_shape=(20000,)))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(300))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(100, activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))
'''
# 3. Model compile
#model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#model.summary()

# 4. Train model
from tensorflow.keras.models import load_model
#hist = model.fit(train_data_features, y_train, epochs=10, batch_size=64)
model = load_model('saved_model.h5')
#model.save('saved_model.h5')

# 생성된 model을 가시화 하기

from IPython.display import SVG
from tensorflow.keras.utils import model_to_dot
from tensorflow.keras.utils import plot_model

#SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
plot_model(model, to_file='model_visualization.png')

# 5. Traing process
'''
fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.set_ylim([0.0, 1.0])
acc_ax.set_ylim([0.0, 1.0])

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
acc_ax.plot(hist.history['accuracy'], 'b', label='train acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()
'''
# 6. Evaluation

loss_and_metrics = model.evaluate(test_data_features, y_test, batch_size=32)
print('loss_and_metrics : ' + str(loss_and_metrics))
print("------[my]test data analysis------")
print(test_data_features.shape)

sub_preds_deep = model.predict(test_data_features,batch_size=32)
print(sub_preds_deep)
while True:
    raw_data = input("type your condition or symptom : ")
    raw_data_frame = pd.DataFrame(columns=['review'])

    test = raw_data_frame.append({'review' : raw_data}, ignore_index=True)
    test['review_clean'] = test['review'].apply(review_to_words)

    print("raw data : ")
    print(test['review'])

    print("cleaned data : ")
    print(test['review_clean'])

    test_data = pipeline.fit_transform(test['review_clean'])
    print(model.predict(test_data, batch_size=32))


#word_table = pd.read_csv("../../../dataset/inquirerbasic.xls")

#Positiv word list
'''
temp_Positiv = []
Positiv_word_list = []
for i in range(0,len(word_table.Positiv)):
    if word_table.iloc[i,2] == "Positiv":
        temp = word_table.iloc[i,0].lower()
        temp1 = re.sub('\d+', '', temp)
        temp2 = re.sub('#', '', temp1)
        temp_Positiv.append(temp2)

Positiv_word_list = list(set(temp_Positiv))
len(temp_Positiv)
len(Positiv_word_list)  #del temp_Positiv

#Negativ word list
temp_Negativ = []
Negativ_word_list = []
for i in range(0,len(word_table.Negativ)):
    if word_table.iloc[i,3] == "Negativ":
        temp = word_table.iloc[i,0].lower()
        temp1 = re.sub('\d+', '', temp)
        temp2 = re.sub('#', '', temp1)
        temp_Negativ.append(temp2)

Negativ_word_list = list(set(temp_Negativ))
len(temp_Negativ)
len(Negativ_word_list)  #del temp_Negativ

vectorizer = CountVectorizer(vocabulary = Positiv_word_list)
content = df_test['review_clean']
X = vectorizer.fit_transform(content)
f = X.toarray()
f = pd.DataFrame(f)
f.columns=Positiv_word_list
df_test["num_Positiv_word"] = f.sum(axis=1)

vectorizer2 = CountVectorizer(vocabulary = Negativ_word_list)
content = df_test['review_clean']
X2 = vectorizer2.fit_transform(content)
f2 = X2.toarray()
f2 = pd.DataFrame(f2)
f2.columns=Negativ_word_list
df_test["num_Negativ_word"] = f2.sum(axis=1)

df_test["Positiv_ratio"] = df_test["num_Positiv_word"]/(df_test["num_Positiv_word"]+df_test["num_Negativ_word"])
df_test["sentiment_by_dic"] = df_test["Positiv_ratio"].apply(lambda x: 1 if (x>=0.5) else (0 if (x<0.5) else 0.5))



'''
