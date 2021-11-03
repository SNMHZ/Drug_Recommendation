from numpy.lib.twodim_base import triu_indices
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
import numpy as np
import pickle
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_model = os.path.join(THIS_FOLDER, 'mymodel/content/test-ynat/checkpoint-2500')
model = AutoModelForSequenceClassification.from_pretrained(my_model)
tokenizer = AutoTokenizer.from_pretrained('google/bert_uncased_L-12_H-512_A-8', use_fast=True)

m_dict_csv = os.path.join(THIS_FOLDER, 'dataset/top20condition.csv')
m_dict = pd.read_csv(m_dict_csv, index_col=0)


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
    top3_ind = np.argpartition(output[0][0], -3)[-3:]
    df_output = pd.DataFrame(output[0][0], columns=['prob'])
    output = pd.concat([m_dict, df_output], axis=1)

    top3 = output.loc[top3_ind].sort_values(by=['prob'], ascending=False)
    top3 = top3.reset_index(drop=True)
    top3 = top3.to_dict('index')

    res_type = 0
    
    drug_list = ['drug_list']

    if res_type == 0:
        symptom_list = None
    
    elif res_type == 1:
        symptom_list = ['symptoms']
    elif res_type == -1:
        symptom_list = None

    result = {
        'res_type': res_type,
        'predict': top3,
        'symptoms': symptom_list
    }
    return result

if __name__=='__main__':
    pred_drug("I have a fever")