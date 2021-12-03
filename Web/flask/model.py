from numpy.lib.twodim_base import triu_indices
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
import numpy as np
import pickle
import os
from mapping_drug import getDrugByCondition

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_model = os.path.join(THIS_FOLDER, 'mymodel/content/test-ynat/checkpoint-2000')
model = AutoModelForSequenceClassification.from_pretrained(my_model)
tokenizer = AutoTokenizer.from_pretrained('google/bert_uncased_L-12_H-512_A-8', use_fast=True)
trainer = Trainer(
        model,
        tokenizer=tokenizer,
    )

condition_numbering_URL = os.path.join(THIS_FOLDER, 'dataset/top20condition.csv')
condition_numbering = pd.read_csv(condition_numbering_URL, index_col=0)

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def preprocess_function(examples):
    return tokenizer(
        examples['review'],
        truncation=True,
        padding=True,
        max_length=184,
        return_token_type_ids=False,
    )
def pred_condition(input_text, seq, n=3):
    test_dict = {'review': input_text}
    test_df = pd.DataFrame(test_dict, index=[0], columns=['review'])
    df_to_dataset = Dataset.from_pandas(test_df)
    encoded_datasets = df_to_dataset.map(preprocess_function, batched=True)
    output = trainer.predict(encoded_datasets)
    res = to_json(output, seq, n)
    
    return res

def to_json(output, seq, n=3):
    cond_prob = softmax(output[0][0])
    #top3_ind = np.argpartition(cond_prob, -3)[-3:]
    res_ind = np.argpartition(cond_prob, -n)[-n:]
    df_output = pd.DataFrame(cond_prob, columns=['prob'])
    output = pd.concat([condition_numbering, df_output], axis=1)

    # top3 = output.loc[top3_ind].sort_values(by=['prob'], ascending=False)
    # top3 = top3.reset_index(drop=True)
    # top3 = top3.to_dict('index')

    predict = output.loc[res_ind].sort_values(by=['prob'], ascending=False)
    predict = predict.reset_index(drop=True)
    predict = predict.to_dict('index')
    
    # type 지정 조건(시나리오)
    
    # if :
    #    res_type = -1
    res_type = 0

    print('--teste--')
    print(predict[0]['prob'], seq)
    print('-tasey-')
    if predict[0]['prob'] <= 0.8 or seq <= 5:
        print("이ㅣ거 실행되야 함!!!")
        res_type = 1

    if res_type == 0:
        symptom_list = None
    elif res_type == 1:
        symptom_list = ['symptoms']
    elif res_type == -1:
        predict = None
        symptom_list = None

    result = {
        'res_type': res_type,
        'predict': predict,
        'symptoms': symptom_list
    }
    return result

if __name__=='__main__':
    # 테스트용 입력
    print(pred_condition("""My boyfriend of 8 years took this medication for migraine for a year and ahalf. It was great for his migraine but hell on his personality and character as a person. This medication made him confused, unable to make decisions, angry because he was confused. He became argumentative with me , coworkers, and family members. Every task he took on was filled with confusion and his ego. In 8 years I never seen him be so cold ..he was not the same person. I thought his behaviour was cause from some other medicine so I convince him to stop. Then the behaviour continued..after reading on this medicine I convince him to drop it. It had been 3 weeks since he took the medication and it&#039;s like night and day.  He is slowly returning to the man I know."""))