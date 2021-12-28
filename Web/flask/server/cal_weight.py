import pandas as pd
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

sym_URL = os.path.join(THIS_FOLDER, 'dataset/sym_onehot.xlsx')
sym_list = pd.read_excel(sym_URL, index_col=0)
MOD_PRED_PLUS = 0.5
MOD_PRED_SUB = 0.2

def cal_weight(predict: dict, yes_list: list, no_list: list):
    # yes +0.1
    # np  -0.1
    for i in range(20):
        for yes in yes_list:
            if sym_list.loc[predict[i]['condition'], yes] == 1:
                predict[i]['prob'] += MOD_PRED_PLUS
        
        for no in no_list:
            if sym_list.loc[predict[i]['condition'], no] == 1:
                predict[i]['prob'] -= MOD_PRED_SUB
    
    return predict

def sort_predict(predict: dict):
    pred_list = sorted(list(predict.values()), key=lambda x: x['prob'], reverse=True)
    pred_dict = dict( [ (i, x) for i, x in enumerate(pred_list) ] )
    return pred_dict

def minmax_prob(predict: dict, mul=10):
    pred_list = list(predict.values())
    min_prob = min(x['prob'] for x in pred_list)
    max_prob = max(x['prob'] for x in pred_list)
    _sum = 0
    for i, x in enumerate(pred_list):
        predict[i]['prob'] = mul**(((predict[i]['prob'] - min_prob) / (max_prob - min_prob))*2)
        _sum += predict[i]['prob']
    for i, x in enumerate(pred_list):
        predict[i]['prob'] /= _sum
    return predict