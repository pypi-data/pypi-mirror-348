#!/usr/bin/env python
# Created by "Thieu" at 16:14, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
import pytest
from unilvq import OptimizedLvq1Classifier


@pytest.fixture
def toy_data():
    X = np.array([
        [0.0, 0.0],
        [0.1, -0.1],
        [-0.1, 0.1],
        [5.0, 5.0],
        [5.1, 4.9],
        [4.9, 5.1]
    ])
    y = np.array([0, 0, 0, 1, 1, 1])
    return X, y


def test_optimized_lvq1_init():
    model = OptimizedLvq1Classifier()
    assert model.n_prototypes_per_class == 1
    assert model.learning_rate == 0.5


def test_optimized_lvq1_fit_predict_score(toy_data):
    X, y = toy_data
    model = OptimizedLvq1Classifier(n_prototypes_per_class=1, initial_learning_rate=0.3, seed=123)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape == y.shape
    acc = model.score(X, y)
    assert 0.0 <= acc <= 1.0


def test_optimized_lvq1_scores(toy_data):
    X, y = toy_data
    model = OptimizedLvq1Classifier(seed=123)
    model.fit(X, y)
    result = model.scores(X, y, list_metrics=["AS", "RS"])
    assert isinstance(result, dict)
    assert "AS" in result
    assert "RS" in result
