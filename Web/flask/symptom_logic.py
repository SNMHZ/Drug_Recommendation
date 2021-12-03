import os 
import pandas as pd
from collections import deque

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sym1_PATH = os.path.join(THIS_FOLDER, 'sym1.pickle')
sym2_PATH = os.path.join(THIS_FOLDER, 'sym2.pickle')
sym1: pd.DataFrame = pd.read_pickle(sym1_PATH)
sym2: pd.DataFrame = pd.read_pickle(sym2_PATH)

# sym1['data'] = sym1['data'].apply(lambda x: deque(x))
# sym2['data'] = sym2['data'].apply(lambda x: deque(x))

def getSymFromSymtableAndNoSym(sym_set, no_sym_set):
    sym_word = ''
    idx = 0
    is_all_empty = 0
    while True:
        if len(sym_set[idx]) == 0:
            is_all_empty = is_all_empty|(1<<idx)
        else:
            intersect = sym_set[idx].intersection(no_sym_set)
            if len( intersect ) > 0:
                sym_set[idx].remove(list(intersect)[0])
            else:
                sym_word = list(sym_set[idx])[0]
                break

        idx+=1
        if idx == 20:
            if is_all_empty == 0b11111111111111111111:
                sym_word = 'error'
                break
            is_all_empty = 0
            idx=0
    return sym_word

def getSymptoms(pr_dict: dict, no_symptoms: list, yes_symptoms: list) -> str:
    sym_word = ''
    yes_len, no_len = len(yes_symptoms), len(no_symptoms)
    seq = yes_len + no_len
    predicts = [ pr_dict[i]['condition'] for i in range(20) ] # list of sorted 20 predictions by the model
    print(predicts)

    ###########################################
    # 첫 seq이면서, 아직 안나온 증상이 있는 경우
    if seq == 0:
        for i in range(20):
            if len(sym1.loc[predicts[i]]['data']) != 0:
                sym_word = sym1.loc[predicts[i]]['data'][0]
                return sym_word
    ###########################################

    # 티어 1 질문인지 티어 2 질문인지 판단
    isTier1 = False if seq > 3 and pr_dict[0]['prob'] > 0.5 else True
    isTier1 = False if seq > 4 and pr_dict[0]['prob'] > 0.4 else True
    isTier1 = False if seq > 5 and pr_dict[0]['prob'] > 0.3 else True


    ###########################################
    # 첫 seq가 아닌 경우
    # 전체 sym1에서 predict0이면, predict0에 있는 sym에서 no_sym이랑 yes_sym에 없는거 넣기.
    # sym1에 predict행에 있는 것 중에서 no_sym이랑 yes_sym에 없는거 넣기.

    no_sym_set = set(no_symptoms)
    yes_sym_set = set(yes_symptoms)
    sym_set = None
    if isTier1:
        sym_set = [ set(sym1.loc[p]['data'])-yes_sym_set for p in predicts ]
    else:
        sym_set = [ set(sym2.loc[p]['data'])-yes_sym_set for p in predicts ]

    sym_word = getSymFromSymtableAndNoSym(sym_set, no_sym_set)
    
    ###########################################

    return sym_word