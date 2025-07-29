"""
QuantumAnomalyDetector
-----------------------
A simple anomaly detection model based on minimum Euclidean distance to training data.

Supports multivariate inputs. Can be used as a classical proxy for quantum behavior.

"""

import numpy as np
from sklearn.neighbors import LocalOutlierFactor

class QuantumAnomalyDetector:
    """
    Improved anomaly detector using Local Outlier Factor (LOF).

    
    Parameters
    k : int
        Number of neighbors for LOF.
    contamination : float
        Expected proportion of outliers.
    model : LocalOutlierFactor
        Underlying scikit-learn LOF model with `novelty=True`.
    """
    def __init__(self, k=20, contamination=0.03):
        self.k = k
        self.contamination = contamination
        self.model = LocalOutlierFactor(
            n_neighbors=self.k,
            contamination=self.contamination,
            novelty=True
        )

    def fit(self, X):
        """
        Fit the LOF model on training data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training feature matrix (assumed mostly normal).
        """
        X = np.asarray(X)
        self.model.fit(X)

    def predict(self, X):
        """
        Compute anomaly scores for new samples.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)

        Returns
        -------
        scores : ndarray, shape (n_samples,)
            Inverted LOF decision function (higher = more anomalous).
        """
        X = np.asarray(X)
        # sklearn's decision_function: higher = more normal, so invert
        return -self.model.decision_function(X)

    def is_anomalous(self, score):
        """
        Determine whether a given score is anomalous.

        Parameters
        ----------
        score : float
            Anomaly score from predict().

        Returns
        -------
        bool
        """
        # model.offset_ is the LOF threshold on decision_function
        return score > -self.model.offset_
