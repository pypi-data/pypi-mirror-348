#!/usr/bin/env python
# Created by "Thieu" at 02:20, 12/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split
from unilvq import EarlyStopper
from unilvq.core.base_model import BaseModel


class CustomGRLVQ(nn.Module):
    """
    Custom implementation of the Generalized Relevance Learning Vector Quantization (GRLVQ) model.

    This class defines a neural network-based GRLVQ model with trainable prototypes,
    relevance matrices, and a custom loss function.

    Attributes
    ----------
    input_dim : int
        The dimensionality of the input data.
    n_prototypes : int
        The number of prototypes used in the model.
    prototypes : torch.nn.Parameter
        A tensor containing the trainable prototypes of shape (n_prototypes, input_dim).
    prototype_labels : torch.nn.Parameter
        A tensor containing the labels of the prototypes, with shape (n_prototypes,).
    relevance : torch.nn.Parameter
        A tensor representing the relevance matrix or vector, depending on the relevance type.
    relevance_type : str
        The type of relevance used ('diag' for diagonal relevance or 'matrix' for full matrix relevance).

    Methods
    -------
    _diag_distance(x):
        Computes the squared Euclidean distance with diagonal relevance weighting.
    _matrix_distance(x):
        Computes the squared Euclidean distance with full matrix relevance weighting.
    forward(x):
        Computes the distances between input samples and prototypes using the specified relevance type.
    grlvq_loss(dists, y_true):
        Computes the GRLVQ loss based on distances and true labels.
    """

    def __init__(self, input_dim, n_prototypes, n_classes, relevance_type='diag', seed=None):
        super().__init__()
        if seed is not None:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
        
        self.input_dim = input_dim
        self.n_prototypes = n_prototypes
        self.prototypes = nn.Parameter(torch.randn(n_prototypes, input_dim))
        self.prototype_labels = nn.Parameter(torch.randint(0, n_classes, (n_prototypes,)), requires_grad=False)
        
        if relevance_type == 'diag':
            self.relevance = nn.Parameter(torch.ones(input_dim))
            self.distance = self._diag_distance
        elif relevance_type == 'matrix':
            self.relevance = nn.Parameter(torch.eye(input_dim))  # Full matrix
            self.distance = self._matrix_distance
        else:
            raise ValueError("relevance_type must be 'diag' or 'matrix'")
    
    def _diag_distance(self, x):
        """
        Computes the squared Euclidean distance with diagonal relevance weighting.
        """
        w = self.relevance.abs()  # enforce positive relevance
        dists = ((x.unsqueeze(1) - self.prototypes.unsqueeze(0)) ** 2) * w
        return dists.sum(dim=2)
    
    def _matrix_distance(self, x):
        """
        Computes the squared Euclidean distance with full matrix relevance weighting.
        """
        W = self.relevance @ self.relevance.T  # positive semi-definite
        diffs = x.unsqueeze(1) - self.prototypes.unsqueeze(0)
        dists = torch.einsum('bij,jk,bik->bi', diffs, W, diffs)
        return dists

    def forward(self, x):
        """
        Computes the distances between input samples and prototypes using the specified relevance type.
        """
        return self.distance(x)

    def grlvq_loss(self, dists, y_true):
        """
        Computes the GRLVQ loss based on distances and true labels.
        """
        batch_size = dists.shape[0]
        y_true = y_true.view(-1, 1)
        proto_labels = self.prototype_labels.expand(batch_size, -1)
        true_mask = (proto_labels == y_true)
        false_mask = ~true_mask

        d_plus = torch.min(dists.masked_fill(~true_mask, float('inf')), dim=1).values
        d_minus = torch.min(dists.masked_fill(~false_mask, float('inf')), dim=1).values

        mu = (d_plus - d_minus) / (d_plus + d_minus + 1e-8)
        return torch.mean(torch.sigmoid(mu))


class GrlvqClassifier(BaseModel, ClassifierMixin):
    """
    Generalized Relevance Learning Vector Quantization (GRLVQ) Classifier.

    This class implements a GRLVQ-based classifier using PyTorch amd Scikit-Learn.
    It supports training with early stopping, validation, and relevance learning for classification tasks.

    Attributes
    ----------
    n_prototypes_per_class : int
        Number of prototypes per class.
    relevance_type : str
        Type of relevance used ('diag' for diagonal relevance or 'matrix' for full matrix relevance).
    epochs : int
        Number of training epochs.
    batch_size : int
        Batch size for training.
    optim : str
        Name of the optimizer to use (e.g., "Adam", "SGD").
    optim_paras : dict
        Parameters for the optimizer.
    early_stopping : bool
        Whether to use early stopping during training.
    n_patience : int
        Number of epochs to wait for improvement before stopping early.
    epsilon : float
        Minimum improvement required to reset early stopping patience.
    valid_rate : float
        Proportion of data to use for validation (between 0 and 1).
    seed : int
        Random seed for reproducibility.
    verbose : bool
        Whether to print training progress.
    device : str
        Device to use for training ("cpu" or "gpu").

    Methods
    -------
    _process_data(X, y):
        Prepares data for training and validation.
    fit(X, y):
        Trains the GRLVQ classifier on the given data.
    predict(X):
        Predicts class labels for the given input data.
    score(X, y):
        Computes the accuracy of the classifier on the given data.
    evaluate(y_true, y_pred, list_metrics=("AS", "RS")):
        Evaluates classification performance using specified metrics.
    scores(X, y, list_metrics=("AS", "RS")):
        Computes classification metrics for the given data.
    """

    def __init__(self, n_prototypes_per_class=1, relevance_type='diag',
                 epochs=1000, batch_size=16, optim="Adam", optim_paras=None,
                 early_stopping=True, n_patience=10, epsilon=0.001, valid_rate=0.1,
                 seed=42, verbose=True, device=None):
        super().__init__()
        self.n_prototypes_per_class = n_prototypes_per_class
        self.relevance_type = relevance_type
        self.epochs = epochs
        self.batch_size = batch_size
        self.optim = optim
        self.optim_paras = optim_paras if optim_paras else {}
        self.early_stopping = early_stopping
        self.n_patience = n_patience
        self.epsilon = epsilon
        self.valid_rate = valid_rate
        self.seed = seed
        self.verbose = verbose
        if device == 'gpu':
            if torch.cuda.is_available():
                self.device = 'cuda'
            else:
                raise ValueError("GPU is not available. Please set device to 'cpu'.")
        else:
            self.device = "cpu"

        self.network, self.optimizer = None, None
        self.early_stopper = None
        self.valid_mode = False

    def _process_data(self, X, y):
        X_valid_tensor, y_valid_tensor, X_valid, y_valid = None, None, None, None

        # Split data into training and validation sets based on valid_rate
        if self.valid_rate is not None:
            if 0 < self.valid_rate < 1:
                # Activate validation mode if valid_rate is set between 0 and 1
                self.valid_mode = True
                X, X_valid, y, y_valid = train_test_split(X, y, test_size=self.valid_rate,
                                                          random_state=self.seed, shuffle=True, stratify=y)
            else:
                raise ValueError("Validation rate must be between 0 and 1.")

        # Convert data to tensors and set up DataLoader
        X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
        y_tensor = torch.tensor(y, dtype=torch.long).to(self.device)
        train_loader = DataLoader(TensorDataset(X_tensor, y_tensor), batch_size=self.batch_size, shuffle=True)

        if self.valid_mode:
            X_valid_tensor = torch.tensor(X_valid, dtype=torch.float32).to(self.device)
            y_valid_tensor = torch.tensor(y_valid, dtype=torch.long).to(self.device)
        return train_loader, X_valid_tensor, y_valid_tensor

    def fit(self, X, y):
        # Set up data
        classes = np.unique(y)
        train_loader, X_valid_tensor, y_valid_tensor = self._process_data(X, y)

        if self.early_stopping:
            # Initialize early stopper if early stopping is enabled
            self.early_stopper = EarlyStopper(patience=self.n_patience, epsilon=self.epsilon)
        # Define model, optimizer, and loss criterion based on task
        self.network = CustomGRLVQ(X.shape[1], len(classes) * self.n_prototypes_per_class, len(classes),
                                   relevance_type=self.relevance_type, seed=self.seed).to(self.device)
        self.optimizer = getattr(torch.optim, self.optim)(self.network.parameters(), **self.optim_paras)

        proto_labels = []
        for c in classes:
            proto_labels.extend([c.item()] * self.n_prototypes_per_class)
        self.network.prototype_labels[:] = torch.tensor(proto_labels, dtype=torch.long, device=self.device)

        # Training loop
        self.loss_train = []
        self.network.train()  # Set model to training mode
        for epoch in range(self.epochs):
            # Initialize total loss for this epoch
            total_loss = 0.0

            # Training step over batches
            for batch_X, batch_y in train_loader:
                self.optimizer.zero_grad()  # Clear gradients

                # Forward pass
                output = self.network(batch_X)
                loss = self.network.grlvq_loss(output, batch_y)  # Compute loss

                # Backpropagation and optimization
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()  # Accumulate batch loss

            # Calculate average training loss for this epoch
            avg_loss = total_loss / len(train_loader)
            self.loss_train.append(avg_loss)

            # Perform validation if validation mode is enabled
            if self.valid_mode:
                self.network.eval()  # Set model to evaluation mode
                with torch.no_grad():
                    val_output = self.network(X_valid_tensor)
                    val_loss = self.network.grlvq_loss(val_output, y_valid_tensor)

                # Early stopping based on validation loss
                if self.early_stopping and self.early_stopper.early_stop(val_loss):
                    print(f"Early stopping at epoch {epoch + 1}")
                    break
                if self.verbose:
                    print(f"Epoch: {epoch + 1}, Train Loss: {avg_loss:.4f}, Validation Loss: {val_loss:.4f}")
            else:
                # Early stopping based on training loss if no validation is used
                if self.early_stopping and self.early_stopper.early_stop(avg_loss):
                    print(f"Early stopping at epoch {epoch + 1}")
                    break
                if self.verbose:
                    print(f"Epoch: {epoch + 1}, Train Loss: {avg_loss:.4f}")

            # Return to training mode for next epoch
            self.network.train()
        return self

    def predict(self, X):
        """Predict the class labels for the input data."""
        X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
        self.network.eval()
        with torch.no_grad():
            output = self.network(X_tensor)  # Get model predictions
            winner_indices = torch.argmin(output, dim=1)  # Find the closest prototype for each sample
            preds = self.network.prototype_labels[winner_indices]  # Get the corresponding labels
        return preds.cpu().numpy()

    def score(self, X, y):
        """Return the accuracy on the given test data and labels."""
        return accuracy_score(y, self.predict(X))

    def evaluate(self, y_true, y_pred, list_metrics=("AS", "RS")):
        """Return the list of classification performance metrics of the prediction.

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
            True values for `X`.

        y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
            Predicted values for `X`.

        list_metrics : list
            You can get classification metrics from Permetrics library: https://permetrics.readthedocs.io/en/latest/pages/classification.html

        Returns
        -------
        results : dict
            The results of the list metrics
        """
        return self._evaluate_cls(y_true=y_true, y_pred=y_pred, list_metrics=list_metrics)

    def scores(self, X, y, list_metrics=("AS", "RS")):
        """Return the list of classification metrics of the prediction.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
           Test samples. For some estimators this may be a precomputed kernel matrix or a list of generic objects instead with shape
           ``(n_samples, n_samples_fitted)``, where ``n_samples_fitted`` is the number of samples used in the fitting for the estimator.

        y : array-like of shape (n_samples,) or (n_samples, n_outputs)
           True values for `X`.

        list_metrics : list, default=("AS", "RS")
           You can get classification metrics from Permetrics library: https://permetrics.readthedocs.io/en/latest/pages/classification.html

        Returns
        -------
        results : dict
           The results of the list metrics
        """
        y_pred = self.predict(X)
        return self.evaluate(y, y_pred, list_metrics)


class GrlvqRegressor(BaseModel, RegressorMixin):
    """
    Generalized Relevance Learning Vector Quantization (GRLVQ) Regressor.

    This class implements a GRLVQ-based regressor using PyTorch and Scikit-Learn.
    It supports training with early stopping, validation, and relevance learning for regression tasks.

    Attributes
    ----------
    n_prototypes : int
        Number of prototypes used in the model.
    relevance_type : str
        Type of relevance used ('diag' for diagonal relevance or 'matrix' for full matrix relevance).
    epochs : int
        Number of training epochs.
    batch_size : int
        Batch size for training.
    optim : str
        Name of the optimizer to use (e.g., "Adam", "SGD").
    optim_paras : dict
        Parameters for the optimizer.
    early_stopping : bool
        Whether to use early stopping during training.
    n_patience : int
        Number of epochs to wait for improvement before stopping early.
    epsilon : float
        Minimum improvement required to reset early stopping patience.
    valid_rate : float
        Proportion of data to use for validation (between 0 and 1).
    seed : int
        Random seed for reproducibility.
    verbose : bool
        Whether to print training progress.
    device : str
        Device to use for training ("cpu" or "gpu").

    Methods
    -------
    _process_data(X, y):
        Prepares data for training and validation.
    fit(X, y):
        Trains the GRLVQ regressor on the given data.
    predict(X):
        Predicts target values for the given input data.
    score(X, y):
        Computes the R^2 score of the regressor on the given data.
    evaluate(y_true, y_pred, list_metrics=("MSE", "MAE")):
        Evaluates regression performance using specified metrics.
    scores(X, y, list_metrics=("MSE", "MAE")):
        Computes regression metrics for the given data.
    """

    def __init__(self, n_prototypes=10, relevance_type='diag',
                 epochs=1000, batch_size=16, optim="Adam", optim_paras=None,
                 early_stopping=True, n_patience=10, epsilon=0.001, valid_rate=0.1,
                 seed=42, verbose=True, device=None):
        super().__init__()
        self.n_prototypes = n_prototypes
        self.relevance_type = relevance_type
        self.epochs = epochs
        self.batch_size = batch_size
        self.optim = optim
        self.optim_paras = optim_paras if optim_paras else {}
        self.early_stopping = early_stopping
        self.n_patience = n_patience
        self.epsilon = epsilon
        self.valid_rate = valid_rate
        self.seed = seed
        self.verbose = verbose
        if device == 'gpu':
            if torch.cuda.is_available():
                self.device = 'cuda'
            else:
                raise ValueError("GPU is not available. Please set device to 'cpu'.")
        else:
            self.device = "cpu"

        self.network, self.optimizer = None, None
        self.early_stopper = None
        self.valid_mode = False

    def _process_data(self, X, y):
        if y.ndim == 1:
            y = y.reshape(-1, 1)
        X_valid_tensor, y_valid_tensor, X_valid, y_valid = None, None, None, None

        # Split data into training and validation sets based on valid_rate
        if self.valid_rate is not None:
            if 0 < self.valid_rate < 1:
                # Activate validation mode if valid_rate is set between 0 and 1
                self.valid_mode = True
                X, X_valid, y, y_valid = train_test_split(X, y, test_size=self.valid_rate,
                                                          random_state=self.seed, shuffle=True)
            else:
                raise ValueError("Validation rate must be between 0 and 1.")

        # Convert data to tensors and set up DataLoader
        X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
        y_tensor = torch.tensor(y, dtype=torch.float32).to(self.device)
        train_loader = DataLoader(TensorDataset(X_tensor, y_tensor), batch_size=self.batch_size, shuffle=True)

        if self.valid_mode:
            X_valid_tensor = torch.tensor(X_valid, dtype=torch.float32).to(self.device)
            y_valid_tensor = torch.tensor(y_valid, dtype=torch.float32).to(self.device)
        return train_loader, X_valid_tensor, y_valid_tensor

    def fit(self, X, y):
        # Set up data
        train_loader, X_valid_tensor, y_valid_tensor = self._process_data(X, y)

        if self.early_stopping:
            # Initialize early stopper if early stopping is enabled
            self.early_stopper = EarlyStopper(patience=self.n_patience, epsilon=self.epsilon)
        # Define model, optimizer, and loss criterion based on task
        self.network = CustomGRLVQ(X.shape[1], self.n_prototypes, n_classes=1,
                                   relevance_type=self.relevance_type, seed=self.seed).to(self.device)
        self.prototype_targets_ = nn.Parameter(torch.rand(self.n_prototypes, 1, device=self.device))
        self.optimizer = getattr(torch.optim, self.optim)(list(self.network.parameters()) + [self.prototype_targets_],
                                                          **self.optim_paras)

        # Start training
        self.loss_train = []
        self.network.train()  # Set model to training mode
        for epoch in range(self.epochs):
            # Initialize total loss for this epoch
            total_loss = 0.0

            # Training step over batches
            for batch_X, batch_y in train_loader:
                self.optimizer.zero_grad()  # Clear gradients

                # Forward pass
                output = self.network(batch_X)
                weights = F.softmax(-output, dim=1)
                y_pred = weights @ self.prototype_targets_
                loss = F.mse_loss(y_pred, batch_y)  # Compute loss

                # Backpropagation and optimization
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()  # Accumulate batch loss

            # Calculate average training loss for this epoch
            avg_loss = total_loss / len(train_loader)
            self.loss_train.append(avg_loss)

            # Perform validation if validation mode is enabled
            if self.valid_mode:
                self.network.eval()  # Set model to evaluation mode
                with torch.no_grad():
                    val_output = self.network(X_valid_tensor)
                    val_weights = F.softmax(-val_output, dim=1)
                    val_pred = val_weights @ self.prototype_targets_
                    val_loss = F.mse_loss(val_pred, y_valid_tensor)

                # Early stopping based on validation loss
                if self.early_stopping and self.early_stopper.early_stop(val_loss):
                    print(f"Early stopping at epoch {epoch + 1}")
                    break
                if self.verbose:
                    print(f"Epoch: {epoch + 1}, Train Loss: {avg_loss:.4f}, Validation Loss: {val_loss:.4f}")
            else:
                # Early stopping based on training loss if no validation is used
                if self.early_stopping and self.early_stopper.early_stop(avg_loss):
                    print(f"Early stopping at epoch {epoch + 1}")
                    break
                if self.verbose:
                    print(f"Epoch: {epoch + 1}, Train Loss: {avg_loss:.4f}")

            # Return to training mode for next epoch
            self.network.train()
        return self

    def predict(self, X):
        """
        Predict the target values for the input data.
        """
        X = torch.tensor(X, dtype=torch.float32).to(self.device)
        dists = self.network(X)
        weights = F.softmax(-dists, dim=1)
        return (weights @ self.prototype_targets_).detach().cpu().numpy()

    def score(self, X, y):
        """
        Returns the coefficient of determination R2 of the prediction.
        """
        return r2_score(y, self.predict(X))

    def evaluate(self, y_true, y_pred, list_metrics=("MSE", "MAE")):
        """
        Returns a list of performance metrics for the predictions.

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
            True values for the input features.
        y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
            Predicted values for the input features.
        list_metrics : list, default=("MSE", "MAE")
            List of metrics to evaluate (can be from Permetrics library: https://github.com/thieu1995/permetrics).

        Returns
        -------
        results : dict
            A dictionary containing the results of the specified metrics.
        """
        return self._evaluate_reg(y_true, y_pred, list_metrics)  # Call the evaluation method

    def scores(self, X, y, list_metrics=("MSE", "MAE")):
        """
        Returns a list of performance metrics for the predictions.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.
        y : array-like of shape (n_samples,) or (n_samples, n_outputs)
            True values for the input features.
        list_metrics : list, default=("MSE", "MAE")
            List of metrics to evaluate (can be from Permetrics library:  https://github.com/thieu1995/permetrics).

        Returns
        -------
        results : dict
            A dictionary containing the results of the specified metrics.
        """
        y_pred = self.predict(X)
        return self.evaluate(y, y_pred, list_metrics)
