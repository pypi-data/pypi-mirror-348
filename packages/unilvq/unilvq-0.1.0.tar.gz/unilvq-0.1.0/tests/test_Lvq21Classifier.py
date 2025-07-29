#!/usr/bin/env python
# Created by "Thieu" at 16:10, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
import pytest
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from unilvq import Lvq21Classifier


@pytest.fixture
def toy_data():
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2, n_informative=2,
                               n_redundant=0, random_state=42)
    return train_test_split(X, y, test_size=0.2, random_state=42)


def test_lvq21_fit_and_predict(toy_data):
    X_train, X_test, y_train, y_test = toy_data
    model = Lvq21Classifier(n_prototypes_per_class=1, learning_rate=0.2, window=0.3, seed=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    assert len(y_pred) == len(y_test)
    assert np.all(np.isin(y_pred, np.unique(y_train)))


def test_lvq21_score(toy_data):
    X_train, X_test, y_train, y_test = toy_data
    model = Lvq21Classifier(n_prototypes_per_class=1, seed=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
