"""
Utility functions used in Activity 6.

Author: Luis Capelo
Date: 2017-12-18
"""
import numpy as np


def create_groups(data, group_size=7):
    """
    Creates distinct groups from a given continuous series.

    Parameters
    ----------
    data: np.array
        Series of continious observations.

    group_size: int, default 7
        Determines how large the groups are. That is,
        how many observations each group contains.

    Returns
    -------
    A Numpy array object. 
    """
    samples = list()
    for i in range(0, len(data), group_size):
        sample = list(data[i:i + group_size])
        if len(sample) == group_size:
            samples.append(np.array(sample).reshape(1, group_size).tolist())

    A = np.array(samples)
    return A.reshape(1, A.shape[0], group_size)

def split_lstm_input(groups):
    """
    Splits groups in a format expected by 
    the LSTM layer. 
    
    Parameters
    ----------
    groups: np.array
        Numpy array with the organized sequences.
    
    Returns
    -------
    X, Y: np.array
        Numpy arrays with the shapes required by
        the LSTM layer. X with (1, a - 1, b)
        and Y with (1, b). Where a is the total
        number of groups in `group` and b the
        number of observations per group.
    """
    X = groups[0:,:-1].reshape(1, groups.shape[1] - 1, groups.shape[2])
    Y = groups[0:,-1:][0]

    return X, Y

def mape(A, B):
    """
    Calcualtes the mean absolute persent error
    from two series. Original solution from:
    
        https://stats.stackexchange.com/questions/58391/\
            mean-absolute-percentage-error-mape-in-scikit-learn
    """
    return np.mean(np.abs((A - B) / A)) * 100

def rmse(A, B):
    """
    Calculates the root mean square error from
    two series. Original solution from:

        https://stackoverflow.com/questions/16774849\
            /mean-squared-error-in-numpy
    """
    return np.sqrt(np.square(np.subtract(A, B)).mean())
