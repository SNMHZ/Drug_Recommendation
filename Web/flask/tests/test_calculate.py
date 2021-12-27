import pytest
#import server.model as model
from server.cal_weight import *
import warnings
from copy import deepcopy
warnings.filterwarnings(action='ignore')

# result = model.pred_condition("i have fever", 0, 20)
predicts = {0: {'condition': 'High Blood Pressure', 'prob': 0.7808085680007935}, 1: {'condition': 'High Cholesterol', 'prob': 0.05836723744869232}, 2: {'condition': 'Sinusitis', 'prob': 0.036744628101587296}, 3: {'condition': 'Muscle Spasm', 'prob': 0.020205944776535034}, 4: {'condition': 'Nausea/Vomiting', 'prob': 0.016527263447642326}, 5: {'condition': 'Bronchitis', 'prob': 0.014082646928727627}, 6: {'condition': 'GERD', 'prob': 0.012092766351997852}, 7: {'condition': 'Rheumatoid Arthritis', 'prob': 0.011834286153316498}, 8: {'condition': 'Cough', 'prob': 0.010977812111377716}, 9: {'condition': 'Underactive Thyroid', 'prob': 0.008199954405426979}, 10: {'condition': 'Back Pain', 'prob': 0.008120283484458923}, 11: {'condition': 'Headache', 'prob': 0.0038420113269239664}, 12: {'condition': 'Fibromyalgia', 'prob': 0.00340442662127316}, 13: {'condition': 'Hepatitis C', 'prob': 0.003361720824614167}, 14: {'condition': 'Constipation', 'prob': 0.0030391961336135864}, 15: {'condition': 'Irritable Bowel Syndrome', 'prob': 0.002888471819460392}, 16: {'condition': 'Osteoarthritis', 'prob': 0.0020210586953908205}, 17: {'condition': 'Migraine', 'prob': 0.001650115940719843}, 18: {'condition': 'Asthma, Maintenance', 'prob': 0.0009395668166689575}, 19: {'condition': 'Allergic Rhinitis', 'prob': 0.0008919868269003928}}
# predicts = result['predict']
yes_list = []
no_list = ['nosebleed']

def test_cal_weight():
    print(predicts)
    predicts_wonbon = deepcopy( predicts)
    cal_weight_out = cal_weight(predicts, yes_list, no_list)
    assert cal_weight_out[0]['prob'] == predicts_wonbon[0]['prob']-MOD_PRED