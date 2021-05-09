import nltk
nltk.download('punkt')
import pandas as pd
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import  cosine_similarity

df_train = pd.read_csv("https://raw.githubusercontent.com/SNMHZ/Drug_Recommendation/master/dataset/lem_train.csv", parse_dates=["date"], infer_datetime_format=True)
df_test = pd.read_csv("https://raw.githubusercontent.com/SNMHZ/Drug_Recommendation/master/dataset/lem_test.csv", parse_dates=["date"], infer_datetime_format=True)

print(type(df_train['review']))

#df_train['tokenize_review'] = word_tokenize(df_train['review'])

print(df_train.isnull().values.any())
print(df_test.isnull().values.any())

print(len(df_train))
print(len(df_test))

df_train = df_train.dropna(how='any')
df_test = df_test.dropna(how='any')

print(df_train.isnull().values.any())
print(df_test.isnull().values.any())

print(len(df_train))
print(len(df_test))
print(df_train['review'][0])

df_train['new'] = df_train['review'].str.cat(df_train['condition'], sep=' ')
df_train['new'] = df_train['new'].str.lower()

# to-do : 증상이 2단어 이상으로 이루어진것도 존재함. 이거 핸들링 해야 함

tokenize_data = [word_tokenize(sentence) for sentence in df_train['new']]

print(tokenize_data[:2])

model = Word2Vec(sentences= tokenize_data, size=100, window=5, min_count=5, workers=4, sg=0)

print(model.wv.vectors.shape)

print(type(model.wv.most_similar('anxiety')))

concon=pd.read_csv('https://raw.githubusercontent.com/SNMHZ/Drug_Recommendation/master/dataset/spaced_conidtion.csv', index_col=0)
ori_con=concon['original'].unique()
mod_con=concon['modified'].unique()

for i in range(len(ori_con)):
    ori_con[i]=re.sub('[^a-zA-Z]',' ',ori_con[i])

for i in range(len(mod_con)):
    mod_con[i]=re.sub('[^a-zA-Z]',' ',mod_con[i])

con_dict={}
for i in range(len(mod_con)):
    con_dict[ori_con[i]]=mod_con[i]

print(con_dict)

con_re = re.compile('(%s)' % '|'.join(con_dict.keys()))

def expand_con(s, con_dict=con_dict):
    def replace(match):
        return con_dict[match.group(0)]
    return con_re.sub(replace, s)

df_train['new100'] = df_train['new'].apply(lambda x: expand_con(x))

tokenize_data2 = [word_tokenize(sentence) for sentence in df_train['new100']]

print(tokenize_data2[:2])

model2 = Word2Vec(sentences= tokenize_data2, size=100, window=5, min_count=5, workers=4, sg=0)

def predictCondition(data):
    result = {}
    # print(words)

    for word in data:
        try:
            tmp = model2.wv.most_similar(word, topn=100)
            print(word)
            # print(len(tmp))
            # print(tmp)
            result[word]= tmp
        except:
            print(word + "not in here\n")
    
    return result

def predictCondition2dict(_predictCondition):
  predict_dict = {}
  for key, value in _predictCondition:
    predict_dict[key] = value
  return predict_dict

def predictCondition_concat(_dict_list):
  sum_dict = {}
  for _dict in _dict_list:
    for key in _dict.keys():
      if key in sum_dict:
        sum_dict[key]+=_dict[key]
      else:
        sum_dict[key]=_dict[key]
  return sum_dict

def predictConditionSum(data):
  predict_res = predictCondition(data)
  m_list = []
  for key in predict_res:
    m_list.append(predictCondition2dict(predict_res[key]))
  return predictCondition_concat(m_list)

from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

n=WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def lemlem(msg):
  msg=msg.replace("&#039;", "")
  msg=msg.replace(r'[^\w\d\s]',' ')
  msg=re.sub('[^a-zA-Z]',' ',msg)
  low_msg = msg.lower().split()
  stop_msg=[]
  for w in low_msg: 
    if w not in stop_words: 
        stop_msg.append(w) 
  result=[n.lemmatize(w) for w in stop_msg]
  return result


only_condition = pd.concat([df_train['condition'], df_test['condition']], axis=0)
only_condition = only_condition.drop_duplicates()
for i in only_condition.index:
    only_condition[i] = only_condition[i].lower()

def isincheck(_str):
  if len(set(only_condition.isin([_str.lower()])))==2:
    return True
  return False

while True:
    msg = input("data : ")

    tmp = predictConditionSum(lemlem(msg))
    m_sorted_res = sorted(list(tmp.items()), key=lambda x:x[1], reverse=True)[:1000]

    for i, res in enumerate(m_sorted_res):
        if isincheck(res[0]):
            print(i, res)