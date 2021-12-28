import os 
import pandas as pd
from collections import deque

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sym1_PATH = os.path.join(THIS_FOLDER, 'sym1.pickle')
sym2_PATH = os.path.join(THIS_FOLDER, 'sym2.pickle')
sym_final = os.path.join(THIS_FOLDER, 'sym_final.pickle')
sym1: pd.DataFrame = pd.read_pickle(sym1_PATH)
sym2: pd.DataFrame = pd.read_pickle(sym2_PATH)
sym_final: pd.DataFrame = pd.read_pickle(sym_final)

msgsym0 = ['frequent mood swings', 'frequent mood swings', 'fever', 'chill', 'headache', 'rash', 'tingling or pain in parts of your body', 'stomach pain', 'diarrhoea', 'constipation', 'blocked nose', 'green or yellow mucus from nose', 'difficulty swallowing', 'trouble coping with stress', 'being unable to stick to tasks that are tedious or time-consuming', 'problems with short-term memory', 'difficulty organising tasks', 'loss of consciousness', 'visual problems such as seeing flashing lights, zig-zag patterns or blind spots', 'redness and swelling of the vulva', 'vaginal rash', 'an overwhelming urge to move your legs', 'pelvic pain', 'pee that looks cloudy', 'pain when peeing', 'weakness and muscle wasting ', 'diarrhoea', 'constipation', 'swollen joints', 'sneezing', 'runny nose', 'reduced sense of smell', 'swelling around eyes, cheeks and nose', 'a burning sensation in chest, usually after eating', 'sensation of a lump in throat', 'tingling or pain in parts of your body', 'lack of coordination or unsteady gait', 'indigestion', 'problems with short-term memory', 'disorganized thinking or speeching', 'delusions', 'aggressive thoughts about losing control and harming yourself or others', 'fear of dirt']
msgsym1 = ['tired', 'loss of appetite', 'emptiness or worthlessness', 'sadness, tearfulness, emptiness or hopelessness', 'poor concentration', 'dizziness', 'poor concentration', 'blurred vision', 'like needing to pee often', 'itching and irritation', 'a burning sensation', 'joint stiffness', 'chest pain', 'illogical thinking, or doing things that often have disastrous consequences', 'pessimistic about everything', 'lacking energy, but also sometimes feeling full of energy', 'guilt and despair', 'loss of interest in everyday activities', 'emptiness or worthlessness', 'appearing forgetful or losing things', 'a short attention span and being easily distracted', 'making careless mistakes', 'appearing to be unable to listen to or carry out instructions', 'constantly changing activity or task', 'moderate or severe throbbing sensation that gets worse when you move or normal activities', 'difficulty speaking', 'poor concentration', 'thirsty all the time', 'a sharp, stabbing pain', 'crackling sound when moving the affected joints', 'uncomfortably full and swollen', 'throbbing and aching pain in joint', 'electric-shock sensations that occur with certain neck movements']
msgsym2 = ['difficulty sleeping', 'vomiting', 'waking up early or not feeling like sleeping', 'sometimes hearing voices that not exist in real life', 'seeing hallucinations', 'having difficulty tolerating uncertainty']

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

    ###########################################
    # 첫 seq이면서, 아직 안나온 증상이 있는 경우
    if seq == 0:
        for i in range(20):
            if len(sym_final.loc[predicts[i]]['data']) != 0:
                sym_word = sym_final.loc[predicts[i]]['data'][0]
                return sym_word
    ###########################################

    ###########################################
    # 첫 seq가 아닌 경우
    # sym에 predict행에 있는 것 중에서 no_sym이랑 yes_sym에 없는거 넣기.
    no_sym_set = set(no_symptoms)
    yes_sym_set = set(yes_symptoms)

    sym_set = [ set(sym_final.loc[p]['data'])-yes_sym_set for p in predicts ]

    sym_word = getSymFromSymtableAndNoSym(sym_set, no_sym_set)
    ###########################################

    return sym_word

# def getSymptoms(pr_dict: dict, no_symptoms: list, yes_symptoms: list) -> str:
#     sym_word = ''
#     yes_len, no_len = len(yes_symptoms), len(no_symptoms)
#     seq = yes_len + no_len
#     predicts = [ pr_dict[i]['condition'] for i in range(20) ] # list of sorted 20 predictions by the model
#     print(predicts)

#     ###########################################
#     # 첫 seq이면서, 아직 안나온 증상이 있는 경우
#     if seq == 0:
#         for i in range(20):
#             if len(sym1.loc[predicts[i]]['data']) != 0:
#                 sym_word = sym1.loc[predicts[i]]['data'][0]
#                 return sym_word
#     ###########################################

#     # 티어 1 질문인지 티어 2 질문인지 판단
#     isTier1 = not (seq > 3 and pr_dict[0]['prob'] > 0.5)
#     isTier1 = not (seq > 4 and pr_dict[0]['prob'] > 0.4) and isTier1
#     isTier1 = not (seq > 5 and pr_dict[0]['prob'] > 0.3) and isTier1


#     ###########################################
#     # 첫 seq가 아닌 경우
#     # 전체 sym1에서 predict0이면, predict0에 있는 sym에서 no_sym이랑 yes_sym에 없는거 넣기.
#     # sym1에 predict행에 있는 것 중에서 no_sym이랑 yes_sym에 없는거 넣기.

#     no_sym_set = set(no_symptoms)
#     yes_sym_set = set(yes_symptoms)
#     sym_set = None
#     if isTier1:
#         sym_set = [ set(sym1.loc[p]['data'])-yes_sym_set for p in predicts ]
#     else:
#         sym_set = [ set(sym2.loc[p]['data'])-yes_sym_set for p in predicts ]

#     sym_word = getSymFromSymtableAndNoSym(sym_set, no_sym_set)
    
#     ###########################################

#     return sym_word

def getCompleteSentenceBySymptom(sym_word):
    if sym_word in msgsym2:
        return 'Are you ' + sym_word + '?'
    if sym_word in msgsym1:
        return 'Do you feel ' + sym_word + '?'
    return 'Do you have ' + sym_word + '?'
    return 'Are you experiencing any symptoms?'

def getSymptomFromFirstMsg(text_body, yes_symptoms: list) -> None:
    for sym in msgsym0+msgsym1+msgsym2:
        if sym in text_body:
            yes_symptoms.append(sym)
            return