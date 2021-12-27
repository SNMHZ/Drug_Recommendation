import pandas as pd
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

sym_URL = os.path.join(THIS_FOLDER, 'dataset/sym_onehot.xlsx')
sym_list = pd.read_excel(sym_URL, index_col=0)
MOD_PRED_PLUS = 0.1
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