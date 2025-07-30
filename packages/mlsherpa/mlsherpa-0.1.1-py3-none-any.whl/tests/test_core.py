import pytest
import pandas as pd
from sklearn.datasets import load_iris, fetch_california_housing
from automl.core import AutoML

@pytest.fixture
def iris_data():
    data = load_iris(as_frame=True)
    df = data.frame
    target = 'target'
    df[target] = data.target
    return df, target, 'classification'

@pytest.fixture
def california_data():
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    target = 'MedHouseVal'
    df[target] = data.target
    return df, target, 'regression'

def test_classification_pipeline(iris_data):
    df, target, problem_type = iris_data
    automl = AutoML(df, target, problem_type)
    best_model = automl.run()
    assert 'name' in best_model
    assert 'score' in best_model

def test_regression_pipeline(california_data):
    df, target, problem_type = california_data
    automl = AutoML(df, target, problem_type)
    best_model = automl.run()
    assert 'name' in best_model
    assert 'score' in best_model
