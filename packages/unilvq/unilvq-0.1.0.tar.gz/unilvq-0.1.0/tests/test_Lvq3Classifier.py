#!/usr/bin/env python
# Created by "Thieu" at 16:12, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
import pytest
from unilvq import Lvq3Classifier


@pytest.fixture
def simple_data():
    X = np.array([
        [1.0, 1.0],
        [1.2, 0.8],
        [0.9, 1.1],
        [3.0, 3.0],
        [3.1, 2.9],
        [2.9, 3.1]
    ])
    y = np.array([0, 0, 0, 1, 1, 1])
    return X, y


def test_lvq3_init():
    model = Lvq3Classifier()
    assert model.n_prototypes_per_class == 1
    assert model.learning_rate == 0.1
    assert model.window == 0.3
    assert model.epsilon == 0.3


def test_lvq3_fit_predict_score(simple_data):
    X, y = simple_data
    model = Lvq3Classifier(n_prototypes_per_class=1, learning_rate=0.2, seed=42)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape == y.shape
    acc = model.score(X, y)
    assert 0.0 <= acc <= 1.0


def test_lvq3_scores(simple_data):
    X, y = simple_data
    model = Lvq3Classifier(seed=42)
    model.fit(X, y)
    result = model.scores(X, y, list_metrics=["AS"])
    assert isinstance(result, dict)
    assert "AS" in result
