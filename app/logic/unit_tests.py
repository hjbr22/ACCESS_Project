import pytest

from gui import get_guis
from jobClass import get_job_classes
from research import get_research_fields

@pytest.mark.integration
def test_get_gui():
    assert get_guis("Jetstream2") == "Exosphere, Horizon, CACAO"

@pytest.mark.integration
def test_get_gui_type():
    assert type(get_guis("Jetstream2")) == str

@pytest.mark.integration
def test_get_job_classes():
    assert get_job_classes("Bridges-2") == "Data Analytics, Machine Learning"

@pytest.mark.integration
def test_get_job_classes_type():
    assert type(get_job_classes("Bridges-2")) == str

def test_get_research_fields():
    assert get_research_fields("KyRIC") == "Agriculture"

def test_get_research_fields_type():
    assert type(get_research_fields("KyRIC")) == str

