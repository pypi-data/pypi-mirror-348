#!/usr/bin/env python
# Created by "Thieu" at 16:22, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import pytest
import numpy as np
from sklearn.datasets import make_regression
from sklearn.metrics import r2_score
import torch
from unilvq import GlvqRegressor


@pytest.fixture
def regression_data():
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
    return X, y


def test_initialization():
    model = GlvqRegressor(epochs=50, n_prototypes=5, device="cpu")
    assert model.n_prototypes == 5
    assert model.device == "cpu"
    assert model.early_stopping is True


def test_invalid_validation_rate():
    with pytest.raises(ValueError, match="Validation rate must be between 0 and 1."):
        model = GlvqRegressor(epochs=50, valid_rate=1.5)
        X, y = np.random.rand(10, 2), np.random.rand(10)
        model.fit(X, y)


def test_invalid_gpu():
    # Only test this if no GPU is available
    if not torch.cuda.is_available():
        with pytest.raises(ValueError, match="GPU is not available"):
            GlvqRegressor(epochs=50, device="gpu")


def test_fit_and_predict_shape(regression_data):
    X, y = regression_data
    model = GlvqRegressor(n_prototypes=3, epochs=10, batch_size=8, device="cpu", verbose=False)
    model.fit(X, y)
    y_pred = model.predict(X)
    assert y_pred.shape == y.reshape(-1, 1).shape


def test_score_accuracy(regression_data):
    X, y = regression_data
    model = GlvqRegressor(n_prototypes=3, epochs=10, batch_size=8, device="cpu", verbose=False)
    model.fit(X, y)
    score_model = model.score(X, y)
    score_true = r2_score(y, model.predict(X))
    assert pytest.approx(score_model, rel=1e-5) == score_true
