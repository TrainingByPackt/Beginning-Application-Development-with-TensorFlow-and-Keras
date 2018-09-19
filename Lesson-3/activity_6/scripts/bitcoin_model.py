"""
Classes and methods for working with a Bitcoin
LSTM model.
"""
import numpy as np

from keras.models import load_model


class BitcoinModel:
    """
    Class that encapsulates the Bitcoin LSTM model
    that we have been building. This class makes it
    easy to work with the different functions
    used to work with the model.
    
    Parameters
    ----------
    path: str
        Location to load model from.

    """
    def __init__(self, model_path):
        self.model_path = model_path
        self.load()
    
    def load(self):
        """
        Loads model from a known location.
        """
        self.model = load_model(self.model_path)
        return self.model
    
    def save(self, path):
        """
        Stores trained model in disk.
        
        Parameters
        ----------
        path: str
            Location of where to store.
        """
        return self.model.save(path)
    
    def create_groups(self, data, group_size=7):
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
        """
        result = last_value * (series + 1)
        return result
    
    def predict(self, X):
        """
        """
        return self.model.predict(x=X)
    
    def train(self):
        """
        """
        self.model.fit()
        pass
    
    def evaluate(self):
        """
        """
        pass
