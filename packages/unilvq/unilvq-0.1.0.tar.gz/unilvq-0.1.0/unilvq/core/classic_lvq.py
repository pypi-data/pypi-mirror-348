#!/usr/bin/env python
# Created by "Thieu" at 02:18, 12/05/2025 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.metrics import accuracy_score
from sklearn.utils import check_random_state
from unilvq.core.base_model import BaseModel


class BaseLVQ(BaseModel):
    """
    A base class for Learning Vector Quantization (LVQ) classifiers.

    This class implements a simple prototype-based classification algorithm where each class is represented
    by a fixed number of prototypes. Classification is performed by assigning the label of the nearest prototype.

    Parameters
    ----------
    n_prototypes_per_class : int, default=1
        Number of prototypes to use per class.

    learning_rate : float, default=0.1
        Learning rate used in learning-based LVQ variants (not utilized in this base class).

    seed : int or None, default=None
        Seed for random number generator to ensure reproducibility.

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        Unique class labels.

    n_classes : int
        Number of unique classes.

    prototypes_ : ndarray of shape (n_classes * n_prototypes_per_class, n_features)
        Coordinates of the prototype vectors.

    prototype_labels_ : ndarray of shape (n_classes * n_prototypes_per_class,)
        Labels assigned to each prototype.

    Methods
    -------
    predict(X)
        Predict class labels for input samples.

    score(X, y)
        Return the mean accuracy on the given test data and labels.

    Notes
    -----
    This is a foundational class for LVQ-based models. It performs initialization of prototypes
    using random selection from training data and supports nearest-prototype classification.
    No learning (weight updates) is performed in this base implementation.
    """

    def __init__(self, n_prototypes_per_class=1, learning_rate=0.1, seed=None):
        super().__init__()
        self.n_prototypes_per_class = n_prototypes_per_class
        self.learning_rate = learning_rate
        self.seed = seed

    def _initialize_prototypes(self, X, y):
        """Initialize prototypes by randomly selecting samples from each class."""
        rng = check_random_state(self.seed)
        self.classes_ = np.unique(y)
        self.n_classes = len(self.classes_)
        self.prototypes_ = []
        self.prototype_labels_ = []

        for cls in self.classes_:
            idx = np.where(y == cls)[0]
            selected = rng.choice(idx, self.n_prototypes_per_class, replace=False)
            self.prototypes_.append(X[selected])
            self.prototype_labels_ += [cls] * self.n_prototypes_per_class

        self.prototypes_ = np.vstack(self.prototypes_)
        self.prototype_labels_ = np.array(self.prototype_labels_)

    def _predict_sample(self, x):
        """Predict the class label for a single sample x."""
        dists = np.linalg.norm(self.prototypes_ - x, axis=1)
        winner = np.argmin(dists)
        return self.prototype_labels_[winner]

    def predict(self, X):
        """Predict class labels for samples in X."""
        return np.array([self._predict_sample(x) for x in X])

    def score(self, X, y):
        """Return the mean accuracy on the given test data and labels."""
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
        return self._evaluate_cls(y_true, y_pred, list_metrics)

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


class Lvq1Classifier(BaseLVQ, ClassifierMixin):
    """
    Learning Vector Quantization 1 (LVQ1) classifier.

    This class implements the LVQ1 algorithm, a prototype-based supervised classification method.
    During training, prototypes are updated incrementally: prototypes of the correct class are moved
    closer to the input sample, while those of the incorrect class are moved further away.

    Inherits from `BaseLVQ`, which provides prototype initialization and prediction methods.

    Parameters
    ----------
    n_prototypes_per_class : int, default=1
        Number of prototypes to initialize per class.

    learning_rate : float, default=0.1
        Learning rate used to update prototypes during training.

    seed : int or None, default=None
        Seed for random number generator for prototype initialization.

    Methods
    -------
    fit(X, y)
        Train the LVQ1 model by updating prototypes based on the training data.

    predict(X)
        Predict class labels for the input samples using nearest prototype rule (inherited).

    score(X, y)
        Compute the accuracy of predictions against true labels (inherited).

    Notes
    -----
    LVQ1 updates only the closest prototype to each input sample. It is sensitive to the learning rate
    and the initialization of prototypes. This implementation uses one-pass stochastic update
    (no epochs or shuffling by default).
    """

    def __init__(self, n_prototypes_per_class=1, learning_rate=0.1, seed=None):
        super().__init__(n_prototypes_per_class, learning_rate, seed)

    def fit(self, X, y):
        """Train the LVQ1 model by updating prototypes based on the training data."""
        self._initialize_prototypes(X, y)
        for xi, yi in zip(X, y):
            dists = np.linalg.norm(self.prototypes_ - xi, axis=1)
            winner_idx = np.argmin(dists)
            winner_label = self.prototype_labels_[winner_idx]

            if winner_label == yi:
                self.prototypes_[winner_idx] += self.learning_rate * (xi - self.prototypes_[winner_idx])
            else:
                self.prototypes_[winner_idx] -= self.learning_rate * (xi - self.prototypes_[winner_idx])
        return self


class Lvq21Classifier(BaseLVQ, ClassifierMixin):
    """
    Learning Vector Quantization 2.1 (LVQ2.1) classifier.

    This class implements the LVQ2.1 algorithm, an extension of LVQ1 that uses competitive updates
    involving the two closest prototypes to a given input. Updates are performed only when the
    input falls within a specified "window" region and when the two closest prototypes belong to
    different classes, one of which must match the input label.

    Parameters
    ----------
    n_prototypes_per_class : int, default=1
        Number of prototypes to initialize per class.

    learning_rate : float, default=0.1
        Learning rate used to update prototypes during training.

    window : float, default=0.3
        Window parameter controlling how close the two nearest prototypes must be (in distance ratio)
        for an update to be performed. Typically between 0.2 and 0.5.

    seed : int or None, default=None
        Seed for random number generator used during prototype initialization.

    Methods
    -------
    fit(X, y)
        Train the LVQ2.1 model by updating prototypes based on the two closest competing prototypes
        and the window condition.

    predict(X)
        Predict class labels for input samples using the nearest prototype (inherited).

    score(X, y)
        Compute the accuracy of the classifier on test data (inherited).

    Notes
    -----
    LVQ2.1 improves classification near decision boundaries by involving two prototypes in the update rule.
    Updates occur only when the distance ratio between the two nearest prototypes falls within
    a specified window, making the algorithm more selective and boundary-aware.
    """

    def __init__(self, n_prototypes_per_class=1, learning_rate=0.1, window=0.3, seed=None):
        super().__init__(n_prototypes_per_class, learning_rate, seed)
        self.window = window

    def fit(self, X, y):
        """Train the LVQ2.1 model by updating prototypes based on the two closest competing prototypes."""
        self._initialize_prototypes(X, y)

        for xi, yi in zip(X, y):
            dists = np.linalg.norm(self.prototypes_ - xi, axis=1)
            idx_sorted = np.argsort(dists)
            i, j = idx_sorted[0], idx_sorted[1]

            label_i, label_j = self.prototype_labels_[i], self.prototype_labels_[j]

            # Check if window condition satisfied
            dist_ratio = dists[i] / dists[j]
            if (label_i != label_j and
                    ((label_i == yi and label_j != yi) or (label_i != yi and label_j == yi)) and
                    ((1 - self.window) <= dist_ratio <= (1 + self.window))):

                if label_i == yi:
                    self.prototypes_[i] += self.learning_rate * (xi - self.prototypes_[i])
                    self.prototypes_[j] -= self.learning_rate * (xi - self.prototypes_[j])
                else:
                    self.prototypes_[i] -= self.learning_rate * (xi - self.prototypes_[i])
                    self.prototypes_[j] += self.learning_rate * (xi - self.prototypes_[j])
        return self


class Lvq3Classifier(BaseLVQ, ClassifierMixin):
    """
    Learning Vector Quantization 3 (LVQ3) classifier.

    This class implements the LVQ3 algorithm, an improvement over LVQ2.1 that introduces a soft update
    mechanism for both winning and second-best prototypes when they belong to different classes and
    at least one of them matches the true label of the input. An additional parameter `epsilon` is used
    to control the adjustment rate of the incorrect prototype.

    Parameters
    ----------
    n_prototypes_per_class : int, default=1
        Number of prototypes initialized for each class.

    learning_rate : float, default=0.1
        Learning rate for updating the correct prototype.

    window : float, default=0.3
        Window parameter controlling the distance ratio condition under which updates occur.
        Must satisfy `0 < window < 1`.

    epsilon : float, default=0.3
        A factor controlling how much the incorrect prototype is updated relative to the correct one.
        Must satisfy `0 <= epsilon <= 1`.

    seed : int or None, default=None
        Seed for the random number generator to ensure reproducibility.

    Methods
    -------
    fit(X, y)
        Train the LVQ3 model using training samples and update rules that involve both the winning
        and second-best prototypes based on class and distance criteria.

    predict(X)
        Predict class labels for input data by assigning the label of the nearest prototype (inherited).

    score(X, y)
        Return the mean classification accuracy on given test data and labels (inherited).

    Notes
    -----
    LVQ3 enhances LVQ2.1 by handling ambiguity near class boundaries more smoothly. When both the closest
    and second-closest prototypes have different labels, and at least one matches the target, both prototypes
    are updated: the correct one is attracted and the incorrect one is repelled slightly. This strategy
    helps to avoid sharp decision boundaries and improves generalization.
    """

    def __init__(self, n_prototypes_per_class=1, learning_rate=0.1, window=0.3, epsilon=0.3, seed=None):
        super().__init__(n_prototypes_per_class, learning_rate, seed)
        self.window = window
        self.epsilon = epsilon

    def fit(self, X, y):
        """Train the LVQ3 model using training samples and update rules."""
        self._initialize_prototypes(X, y)

        for xi, yi in zip(X, y):
            dists = np.linalg.norm(self.prototypes_ - xi, axis=1)
            idx_sorted = np.argsort(dists)
            i, j = idx_sorted[0], idx_sorted[1]

            label_i, label_j = self.prototype_labels_[i], self.prototype_labels_[j]
            dist_ratio = dists[i] / dists[j]

            if label_i != label_j and ((1 - self.window) <= dist_ratio <= (1 + self.window)):
                # Nếu cả hai prototype đều khác class với yi thì bỏ qua
                if label_i == yi and label_j != yi:
                    self.prototypes_[i] += self.learning_rate * (xi - self.prototypes_[i])
                    self.prototypes_[j] -= self.epsilon * self.learning_rate * (xi - self.prototypes_[j])
                elif label_j == yi and label_i != yi:
                    self.prototypes_[j] += self.learning_rate * (xi - self.prototypes_[j])
                    self.prototypes_[i] -= self.epsilon * self.learning_rate * (xi - self.prototypes_[i])
                elif label_i != yi and label_j != yi:
                    # No update, both are incorrect
                    continue
        return self


class OptimizedLvq1Classifier(BaseLVQ, ClassifierMixin):
    """
    Optimized Learning Vector Quantization 1 (LVQ1) classifier with adaptive learning rates.

    This classifier extends the basic LVQ1 algorithm by introducing a per-prototype adaptive learning rate
    that decays over time. Each prototype starts with an initial learning rate and gradually reduces its
    update magnitude after each interaction, improving stability and convergence in noisy or complex datasets.

    Parameters
    ----------
    n_prototypes_per_class : int, default=1
        Number of prototypes to initialize for each class.

    initial_learning_rate : float, default=0.5
        Initial learning rate for prototype updates.

    learning_decay : float, default=0.99
        Multiplicative decay factor applied to each prototype’s learning rate after each update.
        Must be in the range (0, 1).

    seed : int or None, default=None
        Random seed for prototype initialization to ensure reproducibility.

    Attributes
    ----------
    prototype_lr_ : ndarray of shape (n_prototypes,)
        Individual learning rates for each prototype, which decay over time.

    Methods
    -------
    fit(X, y)
        Train the Optimized LVQ1 model by updating prototypes with adaptive learning rates.

    predict(X)
        Predict class labels for input data using the nearest prototype rule (inherited).

    score(X, y)
        Return the mean accuracy of the classifier on test data (inherited).

    Notes
    -----
    By applying a decaying learning rate per prototype, this variant mitigates the risk of overshooting
    optimal prototype positions and enhances convergence. It is particularly effective when training
    on data with overlapping classes or outliers.
    """

    def __init__(self, n_prototypes_per_class=1, initial_learning_rate=0.5, learning_decay=0.99, seed=None):
        super().__init__(n_prototypes_per_class, initial_learning_rate, seed)
        self.learning_decay = learning_decay

    def fit(self, X, y):
        """Train the Optimized LVQ1 model by updating prototypes with adaptive learning rates."""
        self._initialize_prototypes(X, y)
        n_prototypes = self.prototypes_.shape[0]
        self.prototype_lr_ = np.full(n_prototypes, self.learning_rate)

        for xi, yi in zip(X, y):
            dists = np.linalg.norm(self.prototypes_ - xi, axis=1)
            winner_idx = np.argmin(dists)
            winner_label = self.prototype_labels_[winner_idx]

            if winner_label == yi:
                delta = self.prototype_lr_[winner_idx] * (xi - self.prototypes_[winner_idx])
                self.prototypes_[winner_idx] += delta
            else:
                delta = self.prototype_lr_[winner_idx] * (xi - self.prototypes_[winner_idx])
                self.prototypes_[winner_idx] -= delta

            self.prototype_lr_[winner_idx] *= self.learning_decay
        return self
