"""
Utility functions used in Activity 6.

Author: Luis Capelo
Date: 2017-12-18
"""
import random
import numpy as np

from matplotlib import pyplot as plt
from keras.callbacks import TensorBoard


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

def train_model(model, X, Y, epochs=100, version=0, run_number=0):
    """
    Shorthand function for training a new model.
    This function names each run of the model
    using the TensorBoard naming conventions.
    
    Parameters
    ----------
    model: Keras model instance
        Compiled Keras model.

    X, Y: np.array
        Series of observations to be used in
        the training process.

    version: int
        Version of the model to run.
    
    run_number: int
        The number of the run. Used in case
        the same model version is run again.
    """
    hash = random.getrandbits(128)
    hex_code = '%032x' % hash
    model_name = 'bitcoin_lstm_v{version}_run_{run_number}_{hex_code}'.format(
        version=version, run_number=run_number, hex_code=hex_code[:6])

    tensorboard = TensorBoard(log_dir='./logs/{}'.format(model_name))
    
    model_history = model.fit(
        x=X, y=Y,
        batch_size=1, epochs=epochs,
        verbose=0, callbacks=[tensorboard],
        shuffle=False)
    
    return model_history

def plot_two_series(A, B, variable, title):
    """
    Plots two series using the same `date` index. 
    
    Parameters
    ----------
    A, B: pd.DataFrame
        Dataframe with a `date` key and a variable
        passed in the `variable` parameter. Parameter A
        represents the "Observed" series and B the "Predicted"
        series. These will be labelled respectivelly. 
    
    variable: str
        Variable to use in plot.
    
    title: str
        Plot title.
    
    """
    plt.figure(figsize=(14,4))
    plt.xlabel('Real and predicted')

    ax1 = A.set_index('date')[variable].plot(
        linewidth=2, color='#d35400', grid=True, label='Observed', title=title)

    ax2 = B.set_index('date')[variable].plot(
        linewidth=2, color='grey', grid=True, label='Predicted')
    
    ax1.set_xlabel("Predicted Week")
    ax1.set_ylabel("Predicted Values")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()

    plt.legend(l1+l2, loc=2)
    plt.show()

def denormalize(reference, series, 
                normalized_variable='close_point_relative_normalization',
                denormalized_variable='close'):
    """
    Denormalizes the values for a given series.
    
    Parameters
    ----------
    reference: pd.DataFrame
        DataFrame to use as reference. This dataframe
        contains both a week index and the USD price
        reference that we are interested on.

    series: 

    normalized_variable: str

    denormalized_variable: str    
    
    Returns
    -------
    A modified DataFrame with the new variable provided
    in `denormalized_variable` parameter.
    """
    week_values = reference[
        reference['iso_week'] == series['iso_week'].values[0]]
    last_value = week_values[denormalized_variable].values[0]
    series[denormalized_variable] = last_value * (series[normalized_variable] + 1)

    return series