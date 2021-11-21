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

m_dict_csv = os.path.join(THIS_FOLDER, 'dataset/top20condition.csv')
m_dict = pd.read_csv(m_dict_csv, index_col=0)

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
def pred_drug(input_text):
    test_dict = {'review': input_text}
    test_df = pd.DataFrame(test_dict, index=[0], columns=['review'])
    df_to_dataset = Dataset.from_pandas(test_df)
    encoded_datasets = df_to_dataset.map(preprocess_function, batched=True)
    trainer = Trainer(
        model,
        tokenizer=tokenizer,
    )
    output = trainer.predict(encoded_datasets)
    res = to_json(output)
    
    return res

def to_json(output):
    cond_prob = softmax(output[0][0])
    top3_ind = np.argpartition(cond_prob, -3)[-3:]
    df_output = pd.DataFrame(cond_prob, columns=['prob'])
    output = pd.concat([m_dict, df_output], axis=1)

    top3 = output.loc[top3_ind].sort_values(by=['prob'], ascending=False)
    top3 = top3.reset_index(drop=True)
    top3 = top3.to_dict('index')
    
    # type 지정 조건(시나리오)
    
    # if :
    #    res_type = -1
    res_type = 0

    if top3[0]['prob'] <= 0.8:
        res_type = 1

    else:
        res_type = 0
    
    if res_type == 0:
        symptom_list = None
    
    elif res_type == 1:
        symptom_list = ['symptoms']

    elif res_type == -1:
        top3 = None
        symptom_list = None

    result = {
        'res_type': res_type,
        'predict': top3,
        'symptoms': symptom_list
    }
    return result

if __name__=='__main__':
    # 테스트용 입력
    print(pred_drug("""Weight loss Cramping Diarrhea Itchy skin Joint and muscle pain Nausea and vomiting Headaches"""))