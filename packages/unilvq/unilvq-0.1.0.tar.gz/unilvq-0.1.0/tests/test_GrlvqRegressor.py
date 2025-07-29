#!/usr/bin/env python
# Created by "Thieu" at 16:27, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import pytest
import numpy as np
from sklearn.datasets import make_regression
import torch
from unilvq import GrlvqRegressor


@pytest.fixture
def sample_data():
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
    return X, y


def test_grlvq_fit_predict_score(sample_data):
    X, y = sample_data
    model = GrlvqRegressor(
        n_prototypes=5,
        epochs=10,
        batch_size=8,
        early_stopping=False,
        valid_rate=0.2,
        verbose=False,
        device="cpu"
    )
    model.fit(X, y)
    preds = model.predict(X)

    assert isinstance(preds, np.ndarray), "Predictions must be a NumPy array"
    assert preds.shape == (X.shape[0], 1), "Prediction shape must be (n_samples, 1)"

    score = model.score(X, y)
    assert isinstance(score, float), "Score must be a float"
    assert -1.0 <= score <= 1.0, "R² score must be in valid range"


def test_grlvq_invalid_valid_rate(sample_data):
    X, y = sample_data
    model = GrlvqRegressor(epochs=50, valid_rate=1.5)
    with pytest.raises(ValueError, match="Validation rate must be between 0 and 1."):
        model.fit(X, y)


def test_grlvq_gpu_not_available(sample_data, monkeypatch):
    X, y = sample_data

    def fake_cuda_available():
        return False

    monkeypatch.setattr(torch.cuda, "is_available", fake_cuda_available)

    with pytest.raises(ValueError, match="GPU is not available. Please set device to 'cpu'."):
        GrlvqRegressor(epochs=50, device="gpu").fit(X, y)
