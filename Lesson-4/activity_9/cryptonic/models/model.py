"""
Creates a deep learning model abstraction.
"""
from datetime import datetime, timedelta

from keras.models import load_model
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation

from cryptonic.models.helper import ModelHelper
from cryptonic.models.normalizations import point_relative_normalization


class Model(ModelHelper):
    """
    Class that encapsulates an LSTM model
    that we have been building. This class makes it
    easy to work with the different functions
    used to work with the model.
    
    Parameters
    ----------
    path: str
        Location to load model from.

    data: pandas DataFrame
        Pandas dataframe with the variable from
        `variable` privided. This is used
        to eventually train and run the model.
    
    variable: str
        Variable to use from `data`.
    
    predicted_period_size: int
        Number of predicted time periods predictions
        to make.
    
    holdout: int, default 0
        Number of periods to hold-out from the 
        training set.

    """
    def __init__(self, data, variable, predicted_period_size, path=None, 
                 holdout=0, normalize=True):

        self.path = path
        self.data = data
        self.variable = variable
        self.predicted_period_size = predicted_period_size
        self.holdout = holdout

        if path:
            self.model = load_model(self.path)

        self.X, self.Y = self.__prepare_data(normalize=normalize)
        self.__extract_last_series_value()

        super().__init__()

    def __extract_last_series_value(self):
        """
        Method for extracting the last value from
        a series prior to normalization. This value
        is then used for denormalizing the set.
        """
        if self.remainder:
            self.last_value = self.data.sort_values('date', ascending=False)\
                                [:-self.remainder][self.variable].values[0]
            
            self.last_date = self.data.sort_values('date', ascending=False)\
                                [:-self.remainder]['date'].values[0]
        else:
            self.last_value = self.data.sort_values('date', ascending=False)\
                                [self.variable].values[0]
            
            self.last_date = self.data.sort_values('date', ascending=False)\
                                [:-self.remainder]['date'].values[0]
    
    def __prepare_data(self, normalize):
        """
        Prepares data for model.

        Parameters
        ----------
        normalize: bool
            If the method should normalize data or not.
            Normalization is done using 

                normalizations.point_relative_normalization()

        Returns
        -------
        X and Y prepared for training.
        """
        series = self.data[self.variable].values
        self.remainder = len(series) % self.predicted_period_size

        groups = self.create_groups(data=series, 
                                    group_size=self.predicted_period_size,
                                    normalize=normalize)
        
        if self.holdout == 0:
            self.holdout_groups = []
        else:
            self.holdout_groups = groups[::-self.holdout]
            groupps = groups[::-self.holdout]

        self.default_number_of_periods = groups.shape[1] - 1

        return self.split_lstm_input(groups)

    def build(self, number_of_periods=None, period_length=7, batch_size=1):
        """
        Builds an LSTM model using Keras. This function
        works as a simple wrapper for a manually created
        model.
        
        Parameters
        ----------
        period_length: int
            The size of each observation used as input.
        
        number_of_periods: int, default None
            The number of periods available in the 
            dataset. If None, the model will be built
            using all available periods - 1 (used for validation).
        
        batch_size: int
            The size of the batch used in each training
            period.
        
        Returns
        -------
        model: Keras model
            Compiled Keras model that can be trained
            and stored in disk.
        """
        if not number_of_periods:
            number_of_periods = self.default_number_of_periods

        self.model = Sequential()
        self.model.add(LSTM(
            units=period_length,
            batch_input_shape=(batch_size, number_of_periods, period_length),
            input_shape=(number_of_periods, period_length),
            return_sequences=False, stateful=False))

        self.model.add(Dense(units=period_length))
        self.model.add(Activation("linear"))

        self.model.compile(loss="mse", optimizer="rmsprop")

        return self.model

    def save(self, path):
        """
        Stores trained model in disk. Useful
        for storing trained models.
        
        Parameters
        ----------
        path: str
            Location of where to store model.
        """
        return self.model.save(path)
    
    def predict(self, denormalized=False, return_dict=False):
        """
        Makes a prediction based on input data.

        Parameters
        ----------
        denormalized: bool, default True
            If method should denormalize data. Method
            will use the normalizations.point_relative_normalization()
        
        return_dict: bool, default False
            If should return dict that can be serializable
            as JSON. Useful for returning prediction
            results with dates as keys.

        """
        predictions = self.model.predict(x=self.X)
        if denormalized:
            predictions = point_relative_normalization(series=predictions, 
                                                       reverse=True, 
                                                       last_value=self.last_value)
        
        dates = []
        base_date = datetime.strptime(self.last_date, '%Y-%m-%d')
        for i in range(1, len(predictions[0] + 1)):
            d = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
            dates.append(d)

        results = []
        for d,p in zip(dates, predictions[0].tolist()):
            results.append({
                'date': d,
                'prediction': round(p, 2)
            })
        
        if return_dict:
            return results
        
        else:
            return predictions[0]

    def train(self, data=None, epochs=300, verbose=0):
        """
        Trains model using data from class. 

        Parameters
        ----------
        X: pandas DataFrame
            Pandas dataframe with `variable` used to
            fir model for the fist time.

        epochs: int
            Number of epochs to train model for.
        
        verbose: int, default 0
            Verbosity level to use. The default (0)
            means that nothing is printed on the
            screen.
        
        Returns
        -------
        Metrics from the model history.
        """
        if data is not None:
            self.data = data
            self.X, self.Y = self.__prepare_data(normalize=self.normalize)
            self.__extract_last_series_value()

        self.train_history = self.model.fit(
            x=self.X, y=self.Y,
            batch_size=1, epochs=epochs,
            verbose=verbose, shuffle=False)

        self.last_trained = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.train_history

    def evaluate(self, metrics=['mse', 'rmse', 'mape']):
        """
        Evaluates model using provided metrics. The evaluation
        """
        y = point_relative_normalization(series=self.Y[0], 
                                         reverse=True, 
                                         last_value=self.last_value)

        results = {}
        for metric in metrics:
            if metric == 'mse':
                r = round(
                        self.mse(A=self.Y[0], B=self.predict()), 2)

            else:
                r = round(
                        getattr(self, metric)(
                        A=self.predict(denormalized=True)[0], 
                        B=y), 2)

            results[metric] = r

        return results
