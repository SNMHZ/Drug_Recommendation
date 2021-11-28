import pandas as pd
import os 
from transformers import pipeline

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
symptoms_PATH = os.path.join(THIS_FOLDER, 'symptoms_table.pickle')
symptoms_mapping = pd.read_pickle(symptoms_PATH)

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

cond_msg = "I think you have "
symp_msg = "Do you have other symptoms like "

def makeCompleteMsg(condition: str, symptom: str) -> str:
    full_text = cond_msg+condition+'. '+symp_msg+symptom
    generated = generator(full_text,  min_length=len( (full_text).split() )+10, max_length=len( (full_text).split() )*2)[0]['generated_text']
    i=len(cond_msg+condition+'. '+symp_msg)
    print(symptom)
    print(generated)
    for c in generated[i:]:
        i+=1
        if c in ['.', '?', '!']:
            break
    return generated[:i]

def getSymptomsByCondition(condition: str, text_body: str) -> tuple[str, str]:
    symptoms = symptoms_mapping['symptoms'][condition]
    for symptom in symptoms:
        if symptom not in text_body:
            return makeCompleteMsg(condition, symptom), symptom
    return makeCompleteMsg(condition, ''), ''