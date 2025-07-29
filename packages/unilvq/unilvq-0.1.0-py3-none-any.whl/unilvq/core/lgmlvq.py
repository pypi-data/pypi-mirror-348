#!/usr/bin/env python
# Created by "Thieu" at 02:20, 12/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.base import ClassifierMixin
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from unilvq import EarlyStopper
from unilvq.core.base_model import BaseModel


class CustomLGMLVQ(nn.Module):
    """
    Custom implementation of the Local Generalized Matrix Learning Vector Quantization (LGMLVQ) model.

    This class defines a neural network-based LGMLVQ model with trainable prototypes, relevance matrices,
    and a custom loss function for classification tasks.

    Attributes
    ----------
    input_dim : int
        The dimensionality of the input data.
    n_prototypes : int
        The number of prototypes used in the model.
    n_classes : int
        The number of classes in the classification task.
    prototypes : torch.nn.Parameter
        A tensor containing the trainable prototypes of shape (n_prototypes, input_dim).
    relevance_matrices : torch.nn.Parameter
        A tensor containing the trainable relevance matrices for each prototype, with shape
        (n_prototypes, input_dim, input_dim).
    prototype_labels : torch.nn.Parameter
        A tensor containing the labels of the prototypes, with shape (n_prototypes,).

    Methods
    -------
    forward(x):
        Computes the distances between input samples and prototypes using the relevance matrices.
    lgmlvq_loss(dists, y_true):
        Computes the LGMLVQ loss based on distances and true labels.
    """

    def __init__(self, input_dim, n_prototypes, n_classes, seed=None):
        super().__init__()
        if seed is not None:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
        self.input_dim = input_dim
        self.n_prototypes = n_prototypes
        self.n_classes = n_classes

        # Prototype vectors
        self.prototypes = nn.Parameter(torch.randn(n_prototypes, input_dim))

        # Each prototype has its own relevance matrix
        self.relevance_matrices = nn.Parameter(torch.stack([torch.eye(input_dim) for _ in range(n_prototypes)]))

        # Prototype labels (non-trainable)
        self.prototype_labels = nn.Parameter(torch.randint(0, n_classes, (n_prototypes,)), requires_grad=False)

    def forward(self, x):
        diffs = x.unsqueeze(1) - self.prototypes.unsqueeze(0)  # (B, P, D)
        W = torch.einsum("pij,pjk->pik", self.relevance_matrices, self.relevance_matrices)  # Ensure PSD
        dists = torch.einsum("bpd,pde,bpe->bp", diffs, W, diffs)
        return dists

    def lgmlvq_loss(self, dists, y_true):
        batch_size = dists.shape[0]
        y_true = y_true.view(-1, 1)
        proto_labels = self.prototype_labels.expand(batch_size, -1)
        true_mask = (proto_labels == y_true)
        false_mask = ~true_mask

        d_plus = torch.min(dists.masked_fill(~true_mask, float('inf')), dim=1).values
        d_minus = torch.min(dists.masked_fill(~false_mask, float('inf')), dim=1).values

        mu = (d_plus - d_minus) / (d_plus + d_minus + 1e-8)
        return torch.mean(mu)


class LgmlvqClassifier(BaseModel, ClassifierMixin):
    """
    Local Generalized Matrix Learning Vector Quantization (LGMLVQ) Classifier.

    This class implements an LGMLVQ-based classifier using PyTorch and Scikit-Learn.
    It supports training with early stopping, validation, and relevance learning for classification tasks.

    Attributes
    ----------
    n_prototypes_per_class : int
        Number of prototypes per class.
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
        Trains the LGMLVQ classifier on the given data.
    predict(X):
        Predicts class labels for the given input data.
    score(X, y):
        Computes the accuracy of the classifier on the given data.
    evaluate(y_true, y_pred, list_metrics=("AS", "RS")):
        Evaluates classification performance using specified metrics.
    scores(X, y, list_metrics=("AS", "RS")):
        Computes classification metrics for the given data.
    """

    def __init__(self, n_prototypes_per_class=1, epochs=1000, batch_size=16,
                 optim="Adam", optim_paras=None,
                 early_stopping=True, n_patience=10, epsilon=0.001, valid_rate=0.1,
                 seed=42, verbose=True, device=None):
        super().__init__()
        self.n_prototypes_per_class = n_prototypes_per_class
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
        self.network = CustomLGMLVQ(input_dim=X.shape[1], n_prototypes=len(classes) * self.n_prototypes_per_class,
                                    n_classes=len(classes), seed=self.seed).to(self.device)
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
                loss = self.network.lgmlvq_loss(output, batch_y)  # Compute loss

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
                    val_loss = self.network.lgmlvq_loss(val_output, y_valid_tensor)

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
