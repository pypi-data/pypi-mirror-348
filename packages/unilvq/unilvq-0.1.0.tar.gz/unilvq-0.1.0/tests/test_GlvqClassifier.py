#!/usr/bin/env python
# Created by "Thieu" at 16:19, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from unilvq import GlvqClassifier


@pytest.fixture
def synthetic_data():
    X, y = make_classification(n_samples=200, n_features=10, n_classes=3, n_informative=6, random_state=42)
    return train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)


def test_fit_predict_score(synthetic_data):
    X_train, X_test, y_train, y_test = synthetic_data

    model = GlvqClassifier(
        n_prototypes_per_class=2,
        epochs=50,
        batch_size=16,
        optim="Adam",
        optim_paras={"lr": 0.01},
        early_stopping=True,
        n_patience=5,
        epsilon=0.001,
        valid_rate=0.2,
        seed=42,
        verbose=False,
        device="cpu"
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    assert len(preds) == len(y_test), "Predicted labels should match the number of test samples"
    assert set(np.unique(preds)).issubset(set(np.unique(y_train))), "Predicted classes should be in training labels"

    acc = model.score(X_test, y_test)
    assert 0.0 <= acc <= 1.0, "Accuracy should be between 0 and 1"


def test_predict_before_fit_raises_error():
    model = GlvqClassifier(verbose=False)
    X = np.random.rand(10, 5)
    with pytest.raises(AttributeError):
        _ = model.predict(X)


def test_invalid_valid_rate_raises_value_error():
    with pytest.raises(ValueError):
        _ = GlvqClassifier(epochs=50, valid_rate=1.5).fit(np.random.rand(10, 5), np.random.randint(0, 2, 10))


def test_device_gpu_unavailable(monkeypatch):
    # Force torch.cuda.is_available to return False
    import torch
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)

    with pytest.raises(ValueError):
        _ = GlvqClassifier(epochs=50, device="gpu")


def test_fit_without_validation(synthetic_data):
    X_train, X_test, y_train, y_test = synthetic_data
    model = GlvqClassifier(epochs=50, valid_rate=None, verbose=False)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    assert preds.shape == y_test.shape


def test_reproducibility(synthetic_data):
    X_train, X_test, y_train, y_test = synthetic_data
    model1 = GlvqClassifier(epochs=50, seed=42, verbose=False)
    model2 = GlvqClassifier(epochs=50, seed=42, verbose=False)
    model1.fit(X_train, y_train)
    model2.fit(X_train, y_train)
    preds1 = model1.predict(X_test)
    preds2 = model2.predict(X_test)
    assert np.array_equal(preds1, preds2), "Predictions should match if seeds are the same"


def test_custom_optimizer(synthetic_data):
    X_train, _, y_train, _ = synthetic_data
    model = GlvqClassifier(epochs=50, optim="SGD", optim_paras={"lr": 0.01}, verbose=False)
    model.fit(X_train, y_train)
    assert model.optimizer is not None
