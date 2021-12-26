import pytest
from server.symptom_logic import *

def test_getCompleteSentenceBySymptom():
    assert getCompleteSentenceBySymptom('tired') == 'Are you tired?'