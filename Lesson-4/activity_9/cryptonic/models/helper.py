"""
Helper class and methods for making manipulating
data for models.
"""
import numpy as np

import cryptonic.models.normalizations as normalizations


class ModelHelper:
    """
    Class with utility functions that aid in 
    the process of training LSTM models with Keras.

    """
    def __init__(self):
        pass

    def create_groups(self, data, start=0, group_size=7, normalize=True):
        """
        Creates distinct groups from a given continuous series.

        Parameters
        ----------
        data: np.array
            Series of continious observations.
        
        start: int
            Starting point for the series. This 
            is used to prune earlier observations
            from the series in case the series is
            too long or too short.

        group_size: int, default 7
            Determines how large the groups are. That is,
            how many observations each group contains.
        
        normalize: bool
            If the method should normalize data or not.
            Normalization is done using 

                normalizations.point_relative_normalization()

        Returns
        -------
        A Numpy array object. 
        """
        samples = list()
        for i in range(0, len(data), group_size):
            sample = list(data[start + i:i + group_size])
            if len(sample) == group_size:
                if normalize:
                    sample = normalizations.point_relative_normalization(sample)

                samples.append(np.array(sample).reshape(1, group_size).tolist())

        A = np.array(samples)
        return A.reshape(1, A.shape[0], group_size)

    def split_lstm_input(self, groups):
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

    def normalize(self):
        """
        Normalizes a series using point-relative normalization.

        Parameters
        ----------

        Returns
        -------
        """
        normalizations.point_relative_normalization()

    def denormalize(self, series, last_value):
        """
        De-normalizes a series using the latest
        value available from data.
        
        Parameters
        ----------
        series: numpy array
            Series with normalized values.
        
        last_value: float
            Numerical value that represents the
            last value from the dataset.
        
        Returns
        -------
        """
        result = last_value * (series + 1)
        return result

    def mape(self, A, B):
        """
        Calcualtes the mean absolute persentage error
        from two series. Original solution from:
        
            https://stats.stackexchange.com/questions/58391/\
                mean-absolute-percentage-error-mape-in-scikit-learn
        """
        return np.mean(np.abs((A - B) / (1 - A))) * 100

    def rmse(self, A, B):
        """
        Calculates the root mean square error from
        two series. Original solution from:

            https://stackoverflow.com/questions/16774849\
                /mean-squared-error-in-numpy
        """
        return np.sqrt(np.square(np.subtract(A, B)).mean())
    
    def mse(self, A, B):
        """
        Calculates the mean square error from
        two series. Original solution from:

            https://stackoverflow.com/questions/16774849\
                /mean-squared-error-in-numpy
        """
        return np.square(np.subtract(A, B)).mean()
