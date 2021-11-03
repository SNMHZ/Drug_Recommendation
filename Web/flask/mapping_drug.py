import pandas as pd

drug_mapping = pd.read_pickle("mapping_table.pickle")

def getDrugByCondition(condition):
  drugs = drug_mapping['drugs'][condition]
  return [ x[0] for x in drugs[:len(drugs) if len(drugs) < 5 else 5] ]