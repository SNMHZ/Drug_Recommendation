import os 
import pandas as pd
from collections import deque

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sym1_PATH = os.path.join(THIS_FOLDER, 'sym1.pickle')
sym2_PATH = os.path.join(THIS_FOLDER, 'sym2.pickle')
sym1: pd.DataFrame = pd.read_pickle(sym1_PATH)
sym2: pd.DataFrame = pd.read_pickle(sym2_PATH)

sym1['data'] = sym1['data'].apply(lambda x: deque(x))
sym2['data'] = sym2['data'].apply(lambda x: deque(x))

def replace_str(x):
    return x.replace(' ', '')

def getSymptoms(predicts: dict, no_symptoms: list, yes_symptoms: list) -> str:
    sym_word = ''
    no_sym_counts = [ (0, i) for i in range(20) ]
    for i in range(20):
        for no_sym in no_symptoms:
            if no_sym in sym1.loc[predicts[i]['condition']]:
                no_sym_counts[i][0] += 1
        if no_sym_counts[i] == 0:
            sym_word = sym1.loc[predicts[i]['condition']]['data'][0]
            break
    
    if sym_word == '':
        no_sym_counts.sort()
        for sym in sym1.loc[predicts[no_sym_counts[0][1]]['condition']]['data']:
            if sym not in no_symptoms:
                sym_word = sym
                break

    return sym_word