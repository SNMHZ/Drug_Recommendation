from flask import Flask, request
from flask_cors import CORS
import nltk
import pandas as pd
import re
from gensim.models import Word2Vec

app = Flask(__name__)
CORS(app)
model2 = Word2Vec.load("model2_word2vec.model")

def predictCondition(data):
    result = {}
    # print(words)

    for word in data:
        try:
            tmp = model2.wv.most_similar(word, topn=100)
            #print(word)
            # print(len(tmp))
            # print(tmp)
            result[word]= tmp
        except:
            #print(word + "not in here\n")
            pass
    
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

only_condition = pd.read_pickle("./only_condition.pkl")
def isincheck(_str):
    if len(set(only_condition.isin([_str.lower()])))==2:
        return True
    return False

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test', methods=['POST'])
def test():
    # msg = request.values['state']
    # tmp = predictConditionSum(lemlem(msg))
    # m_sorted_res = sorted(list(tmp.items()), key=lambda x:x[1], reverse=True)[:1000]
    # r_msg=''
    # for i, res in enumerate(m_sorted_res):
    #     if isincheck(res[0]):
    #         print(i, res)
    #         r_msg+=res[0]+' '
    msg = request.get_json(force=True)

    tmp = predictConditionSum(lemlem(msg['text']))
    m_sorted_res = sorted(list(tmp.items()), key=lambda x:x[1], reverse=True)[:1000]
    r_msg=''
    for i, res in enumerate(m_sorted_res):
        if isincheck(res[0]):
            r_msg+=res[0]+' '

    return {
        "text" : r_msg
    }


if __name__ == '__main__':
    app.debug = True
    app.run()