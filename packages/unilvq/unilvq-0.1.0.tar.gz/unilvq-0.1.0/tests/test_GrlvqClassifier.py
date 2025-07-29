#!/usr/bin/env python
# Created by "Thieu" at 16:26, 15/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import pytest
import numpy as np
import torch
from sklearn.datasets import make_classification
from unilvq import GrlvqClassifier  # Replace with the actual import path


@pytest.fixture
def sample_data():
    X, y = make_classification(n_samples=100, n_features=4, n_classes=3,
                               n_informative=3, n_redundant=0, random_state=42)
    return X, y


def test_grlvq_init_cpu(sample_data):
    clf = GrlvqClassifier(device='cpu')
    assert clf.device == 'cpu'
    assert clf.n_prototypes_per_class == 1
    assert clf.relevance_type == 'diag'
    assert clf.epochs == 1000
    assert clf.valid_mode is False


def test_grlvq_invalid_device():
    with pytest.raises(ValueError):
        GrlvqClassifier(epochs=50, device='gpu')  # Assuming no GPU is available


def test_process_data_shape(sample_data):
    X, y = sample_data
    clf = GrlvqClassifier(epochs=50, valid_rate=0.2)
    loader, X_val_tensor, y_val_tensor = clf._process_data(X, y)

    for batch_X, batch_y in loader:
        assert isinstance(batch_X, torch.Tensor)
        assert isinstance(batch_y, torch.Tensor)
        break  # Check only one batch

    assert isinstance(X_val_tensor, torch.Tensor)
    assert isinstance(y_val_tensor, torch.Tensor)
    assert X_val_tensor.shape[0] == y_val_tensor.shape[0]


def test_fit_predict_score(sample_data):
    X, y = sample_data
    clf = GrlvqClassifier(epochs=10, valid_rate=0.1, early_stopping=True, verbose=False)
    clf.fit(X, y)
    y_pred = clf.predict(X)
    assert isinstance(y_pred, np.ndarray)
    assert y_pred.shape == y.shape
    acc = clf.score(X, y)
    assert 0.0 <= acc <= 1.0


def test_no_validation_mode(sample_data):
    X, y = sample_data
    clf = GrlvqClassifier(epochs=50, valid_rate=None, early_stopping=False, verbose=False)
    clf.fit(X, y)
    assert not clf.valid_mode
    assert clf.loss_train  # Should have some recorded losses


def test_predict_consistency(sample_data):
    X, y = sample_data
    clf = GrlvqClassifier(epochs=20, valid_rate=0.1, early_stopping=True, verbose=False)
    clf.fit(X, y)
    y_pred1 = clf.predict(X)
    y_pred2 = clf.predict(X)
    assert np.array_equal(y_pred1, y_pred2)


def test_score_output(sample_data):
    X, y = sample_data
    clf = GrlvqClassifier(epochs=10, verbose=False)
    clf.fit(X, y)
    score = clf.score(X, y)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
