"""
Functions to start and configure the Flask
application. This simply configures the server
and its routes.
"""
import os
import flask

from flask_caching import Cache
from flask_cors import CORS, cross_origin

from cryptonic import Model
from cryptonic import CoinMarketCap
from cryptonic.api.routes import create_routes

UI_DIST_DIRECTORY = os.getenv('UI_DIST_DIRECTORY', '../cryptonic-ui/dist/')


class Server:
    """
    Cryptonic server representation. This class
    contains logic for managing the configuration
    and deployment of Flask server.

    Parameters
    ----------
    debug: bool, default False
        If should start with a debugger.

    cors: bool, default True
        If the application should accept CORS
        requests.

    """
    def __init__(self, debug=False, cors=True):
        self.debug = debug
        self.cors = cors

        self.create_model()
        self.app = self.create()

    def create_model(self):
        """
        Creates a model either using a model provided
        by user or by creating a new model using
        previously researched parameters.

        Returns
        -------
        Trained Keras model. Ready to be used 
        via the model.predict() method.
        """
        historic_data = CoinMarketCap.historic(start=os.getenv('BITCOIN_START_DATE', '2017-01-01'))
        model_path = os.getenv('MODEL_NAME')

        #
        #  TODO: Figure out how large the data is for
        #  the old model and re-train. Maybe what I have
        #  to do here is to copy the weights of the
        #  model into a new model.
        #

        self.model = Model(data=historic_data,
                           path=model_path,
                           variable='close',
                           predicted_period_size=int(os.getenv('PERIOD_SIZE', 7)))

        if not model_path:
            self.model.build()
            self.model.train(epochs=int(os.getenv('EPOCHS', 300)), verbose=1)

        return self.model

    def create(self):
        """
        Method for creating a Flask server.

        Returns
        -------
        A Flask() application object.
        """
        app = flask.Flask(__name__, static_url_path='/', static_folder=UI_DIST_DIRECTORY)

        #
        #  Application configuration. Here we
        #  configure the application to accept
        #  CORS requests, its routes, and
        #  its debug flag.
        #
        if self.cors:
            CORS(app)

        cache_configuration = {
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': os.getenv('REDIS_URL',
                                         'redis://redis@cache:6379/0')
        }

        self.cache = Cache(app, config=cache_configuration)

        app.config['DEBUG'] = self.debug
        create_routes(app, self.cache, self.model)

        return app

    def run(self, *args, **kwargs):
        """
        Method for running Flask server.
        Parameters
        ----------
        *args, **kwargs: parameters passed to the Flask application. 
        """
        self.app.run(*args, **kwargs)