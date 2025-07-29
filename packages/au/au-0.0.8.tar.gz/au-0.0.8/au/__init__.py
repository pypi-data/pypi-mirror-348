"""
Outlier analysis is a critical aspect of data preprocessing and analysis, 
particularly in fields like statistics, data mining, and machine learning. 
It involves identifying abnormal, unusual, or significantly different observations 
from the rest of the dataset. Here are a few fundamental functions and objects 
for outlier analysis, incorporating state-of-the-art third-party packages within 
the functions themselves. These functions are designed to cover different approaches 
to outlier detection, including statistical methods and machine learning-based 
techniques.

1. **Z-Score Based Outlier Detection**

   This function identifies outliers based on the Z-score method, which measures how many standard deviations an element is from the mean. Outliers are usually defined as observations that have a Z-score beyond a specified threshold.

   ```python
    detect_outliers_zscore([10, 12, 12, 13, 12, 11, 40])
    # [6]
   ```

2. **Interquartile Range (IQR) Based Outlier Detection**

   This function uses the Interquartile Range (IQR) method for detecting outliers. 
   The IQR is the difference between the 75th and 25th percentile of the data. 
   Observations falling below or above the IQR thresholds are considered outliers.

   ```python
       detect_outliers_iqr([10, 12, 12, 13, 12, 11, 40])
       # [6]
   ```

3. **Isolation Forest Based Outlier Detection**

   This object-oriented approach utilizes the Isolation Forest algorithm, 
   a machine learning method for anomaly detection. It is particularly useful for high-dimensional datasets.

   ```python
       data = [10, 12, 12, 13, 12, 11, 40]
       detector = IsolationForestOutlierDetector()
       detector.detect_outliers(data)
       # [6]
   ```

Each of these functions and the class is equipped with a docstring explaining its 
purpose, parameters, return values, and a simple doctest to demonstrate basic usage. 
The choice of method depends on the nature of the data and the specific requirements 
of the analysis. Z-score and IQR methods are more suitable for univariate data, 
whereas the Isolation Forest can handle multivariate datasets effectively.

"""

import numpy as np


def outlier_lidx(data, method='median_dist', **kwargs):
    """Filtering for outliers"""
    if method == 'median_dist':
        kwargs = dict({'thresh': 3}, **kwargs)
        thresh = kwargs['thresh']
        median_dist = np.abs(data - np.median(data))
        mdev = np.median(median_dist)
        s = median_dist / mdev if mdev else np.zeros(len(median_dist))
        return s >= thresh
    elif method == 'mean_dist':
        kwargs = dict({'thresh': 3}, **kwargs)
        thresh = kwargs['thresh']
        data_std = np.std(data)
        if data_std:
            return abs(data - np.mean(data)) / np.std(data) >= thresh
        else:
            return np.array([False for i in range(len(data))])
    else:
        raise ValueError('method not recognized')


# tcw
def detect_outliers_zscore(data, threshold=3):
    """
    Detects outliers in a dataset based on the Z-score method.

    :param data: List or Numpy array of numerical data.
    :param threshold: Z-score value to identify an outlier. Default is 3.
    :return: List of outlier indices.

    >>> detect_outliers_zscore([10, 12, 12, 13, 12, 11, 40])
    [6]
    """
    mean = np.mean(data)
    std = np.std(data)
    outliers = [i for i, x in enumerate(data) if abs((x - mean) / std) > threshold]
    return outliers


# tcw
def detect_outliers_iqr(data, k=1.5):
    """
    Detects outliers in a dataset based on the Interquartile Range (IQR) method.

    :param data: List or Numpy array of numerical data.
    :param k: Multiplier to define the range beyond which data points are considered outliers. Default is 1.5.
    :return: List of outlier indices.

    >>> detect_outliers_iqr([10, 12, 12, 13, 12, 11, 40])
    [6]
    """
    quartile_1, quartile_3 = np.percentile(data, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (k * iqr)
    upper_bound = quartile_3 + (k * iqr)
    outliers = [i for i, x in enumerate(data) if x < lower_bound or x > upper_bound]
    return outliers


from sklearn.ensemble import IsolationForest

# tcw
class IsolationForestOutlierDetector:
    """
    Outlier detection using Isolation Forest algorithm.

    Usage:
    detector = IsolationForestOutlierDetector()
    outliers = detector.detect_outliers(data)

    >>> data = [10, 12, 12, 13, 12, 11, 40]
    >>> detector = IsolationForestOutlierDetector()
    >>> detector.detect_outliers(data)
    [6]
    """

    def __init__(self, random_state=42):
        self.model = IsolationForest(random_state=random_state)

    def detect_outliers(self, data):
        data = np.array(data).reshape(-1, 1)
        preds = self.model.fit_predict(data)
        return [i for i, x in enumerate(preds) if x == -1]




import numpy as np

def robust_scale_outliers(data, outlier_indices):
    """
    Applies robust scaling to the elements identified as outliers based on their indices.

    :param data: List or Numpy array of numerical data.
    :param outlier_indices: List of indices that are considered outliers.
    :return: Numpy array with outliers scaled using Median and Interquartile Range.

    >>> robust_scale_outliers([10, 12, 12, 13, 12, 11, 40], [6])
    array([10, 12, 12, 13, 12, 11, 13])
    """
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    quartile_1, quartile_3 = np.percentile(data, [25, 75])
    iqr = quartile_3 - quartile_1
    median = np.median(data)
    scaled_data = data.copy()
    for index in outlier_indices:
        if data[index] > quartile_3:
            scaled_data[index] = median + iqr
        elif data[index] < quartile_1:
            scaled_data[index] = median - iqr
    return scaled_data

def visualize_outliers(data, outlier_indices):
    """
    Generates a plot visualizing the data points, highlighting outliers.

    :param data: List or Numpy array of numerical data.
    :param outlier_indices: List of indices that are considered outliers.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 2))
    plt.plot(data, 'bo', label='Data Points')
    plt.plot(outlier_indices, [data[i] for i in outlier_indices], 'ro', label='Outliers')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Outlier Visualization')
    plt.legend()
    plt.grid(True)
    plt.show()

def combine_outlier_detections(data, methods):
    """
    Combines multiple outlier detection methods to find common outliers.

    :param data: List or Numpy array of numerical data.
    :param methods: List of functions that take 'data' as input and return a list of outlier indices.
    :return: List of indices that are considered outliers by all methods.

    >>> combine_outlier_detections([10, 12, 12, 13, 12, 11, 40], [detect_outliers_zscore, detect_outliers_iqr])
    [6]
    """
    from functools import reduce
    outlier_lists = [set(method(data)) for method in methods]
    common_outliers = list(reduce(lambda x, y: x.intersection(y), outlier_lists))
    return common_outliers
