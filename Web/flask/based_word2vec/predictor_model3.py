import nltk
import numpy as np
import pandas as pd
import re
from gensim.models import Word2Vec
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

model = Word2Vec.load("model3_word2vec.model")


def predictCondition(data):
    result = {}
    # print(words)

    for word in data:
        try:
            tmp = model.wv.most_similar(word, topn=100)
            print(word)
            # print(len(tmp))
            # print(tmp)
            result[word]= tmp
        except:
            print(word + " not in here")
            pass
    return result


def predictCondition2dict(_predictCondition):
    predict_dict = {}
    for key, value in _predictCondition:
        predict_dict[key] = value
    return predict_dict

mod_con = np.load('mod_con.npy', allow_pickle=True)
cond_norm = pd.read_pickle("cond_norm.pkl")
def predictCondition_concat(_dict_list):
  sum_dict = {}
  for _dict in _dict_list:
    for key in _dict.keys():
      if key in mod_con:
        if key in sum_dict:
          #print(_dict[key])
          sum_dict[key]+=(_dict[key]*cond_norm[key])
        else:
          #print(key, _dict[key])
          sum_dict[key]=(_dict[key]*cond_norm[key])
          #print(sum_dict[key])
  return sum_dict

def predictConditionSum(data):
    predict_res = predictCondition(data)
    m_list = []
    for key in predict_res:
        m_list.append(predictCondition2dict(predict_res[key]))
    return predictCondition_concat(m_list)

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

only_condition = pd.read_pickle("./only_condition.pkl")
def isincheck(_str):
    if len(set(only_condition.isin([_str.lower()])))==2:
        return True
    return False

condition3 = pd.read_pickle("condition3.pkl")
condition_drugName_rating = pd.read_pickle("condition_drugName_rating.pkl")
def findDrugName(condition):
    tempIndex = (condition3 == condition.lower())
    # 해당 컨디션 단어와 완전 일치하는 경우 약이 매칭 되도록 함
    #tempIndex = df_all['condition_lower'].str.contains(condition.lower())
    # 해당 컨디션 단어가 들어만 가도 약이 매칭 되도록 함
    #print("data type is = ", type(df_all))
    tempSet = condition_drugName_rating[tempIndex]

    result = tempSet.sort_values(by=['rating'], axis=0, ascending=False)
    result=result.groupby(['drugName'], as_index=False).mean()
    result=result.sort_values(by=['rating'], axis=0, ascending=False)

    print("condition is ", condition, '\n',result['drugName'][:5],"\n=====================")
    r_msg = ''
    for i, drName in enumerate(result['drugName'][:5]):
        r_msg+='  %d.'%(i+1)+drName
    print(r_msg)
    return r_msg