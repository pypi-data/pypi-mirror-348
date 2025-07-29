#!/usr/bin/env python
# Created by "Thieu" at 16:32, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from unilvq import LgmlvqClassifier


@pytest.fixture
def dummy_data():
    X, y = make_classification(n_samples=100, n_features=10, n_classes=3, n_informative=5, random_state=42)
    return train_test_split(X, y, test_size=0.2, random_state=42)


def test_initialization():
    model = LgmlvqClassifier()
    assert model.n_prototypes_per_class == 1
    assert model.epochs == 1000
    assert model.device in ["cpu", "cuda"]


def test_fit(dummy_data):
    X_train, X_test, y_train, y_test = dummy_data
    model = LgmlvqClassifier(epochs=10, valid_rate=0.2, early_stopping=True, verbose=False)
    model.fit(X_train, y_train)
    assert model.network is not None
    assert isinstance(model.loss_train, list)
    assert len(model.loss_train) > 0


def test_predict(dummy_data):
    X_train, X_test, y_train, y_test = dummy_data
    model = LgmlvqClassifier(epochs=10, valid_rate=0.2, verbose=False)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    assert preds.shape == y_test.shape
    assert preds.dtype == np.int64


def test_score(dummy_data):
    X_train, X_test, y_train, y_test = dummy_data
    model = LgmlvqClassifier(epochs=10, valid_rate=0.2, verbose=False)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    assert 0.0 <= acc <= 1.0


def test_invalid_valid_rate():
    X, y = make_classification(n_samples=50, n_features=5, n_classes=2, random_state=42)
    model = LgmlvqClassifier(epochs=50, valid_rate=1.5)
    with pytest.raises(ValueError):
        model.fit(X, y)
