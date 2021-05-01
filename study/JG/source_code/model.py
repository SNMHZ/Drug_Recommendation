import nltk
import pandas as pd
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.models import Word2Vec
from konlpy.tag import Okt
from sklearn.metrics.pairwise import  cosine_similarity

df_train = pd.read_csv("../../../dataset/lem_train.csv", parse_dates=["date"], infer_datetime_format=True)
df_test = pd.read_csv("../../../dataset/lem_test.csv", parse_dates=["date"], infer_datetime_format=True)

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

print(model.wv.most_similar('depression'))

def predictCondition(data):
    words = data.split
    print(words)

    for word in words:
        

'''
def vectors(document_list):
    document_embedding_list = []

    for line in document_list:
        doc2vec = None
        count = 0
        for word in line.split():
            if word in model.wv.vocab:
                count += 1
                if doc2vec is None:
                    doc2vec = model[word]
                else:
                    doc2vec = doc2vec + model[word]

        if doc2vec is not None:
            doc2vec = doc2vec/count
            document_embedding_list.append(doc2vec)

    return document_embedding_list

document_embedding_list = vectors(df_train['review'])
print("vectors in doc : ", len(document_embedding_list))

cosine_similarities = cosine_similarity(document_embedding_list, document_embedding_list)
print(cosine_similarities)

def findCondition(data):
    pass
'''