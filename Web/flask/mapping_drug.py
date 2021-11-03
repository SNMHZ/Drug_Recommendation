import pandas as pd
import os 

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
drug_dict = os.path.join(THIS_FOLDER, 'mapping_table.pickle')
drug_mapping = pd.read_pickle(drug_dict)

def getDrugByCondition(condition):
    drugs = drug_mapping['drugs'][condition]
    return [ x[0] for x in drugs[:len(drugs) if len(drugs) < 5 else 5] ]