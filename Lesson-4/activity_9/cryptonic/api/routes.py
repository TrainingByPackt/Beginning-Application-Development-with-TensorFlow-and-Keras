"""
Creates all application routes.
"""
import os

from datetime import datetime, timedelta
from flask_api import status as http_status
from flask import jsonify, request, make_response, send_file, send_from_directory

from cryptonic.api import __version__


def __cache_identifier(*args, **kwargs):
    """
    Creates a cache identifier based on the complete
    URL provided in the request. Original solution:

        * https://stackoverflow.com/questions/9413566/\
            flask-cache-memoize-url-query-string-parameters-as-well
    
    """
    #
    #  The following snippet will create a
    #  cache key for the URL and all GET and POST
    #  parameters.
    #
    key = request.url + \
          '='.join([k + '=' + v for k,v in request.args.items()]) + '&' + \
          '='.join([k + '=' + v for k,v in request.form.items()])

    return key


def create_routes(app, cache, model):
    """
    Function that creates the application routes.

    Parameters
    ----------
    app: Flask object
        Initialized Flask object.
    
    cache: Flask-Caching instance
        Cache instance that can be used
        as a decorator.
    
    model: instantiated Model()
        Module() class instantiated as a model
        and trained.

    Returns
    -------
    app: Flask object
        Modified Flask app object.
    """
    #
    #  Let's clear the cache at every
    #  startup.
    #
    cache.clear()

    @cache.cached(timeout=60 * 5, key_prefix=__cache_identifier)
    @app.errorhandler(404)
    def page_not_found(e):
        return app.send_static_file('index.html'), 404

    @cache.cached(timeout=60 * 5, key_prefix=__cache_identifier)
    @app.route('/')
    def root():
        """
        Endpoint for serving the index page.
        """
        return app.send_static_file('index.html')

    @app.route('/<path:path>')
    def send_static_files(path):
        return send_from_directory(
            os.getenv('UI_DIST_DIRECTORY', '../cryptonic-ui/dist/'), path)

    @app.route('/status')
    def status():
        """
        Endpoint for returning the application status.
        """
        r = {
            'version': __version__,
            'success': True,
            'message': 'Predict Bitcoin prices with deep learning.',
            'model': {
                'name': os.getenv('MODEL_NAME'),
                'last_trained': model.last_trained,
                'error_rates': model.evaluate()
            }
        }
        return jsonify(r)

    @cache.cached(timeout=60 * 24, key_prefix=__cache_identifier)
    @app.route('/historic')
    def historic():
        """
        Returns a series of historic observations.

        Parameters
        ----------
        start: str, default six months ago
            Start date to filter the Bitcoin historic price
            data set.

        """
        six_months_ago = (
            datetime.now() - timedelta(days=30 * 6)).strftime('%Y-%m-%d')
        start = request.args.get('start', six_months_ago)

        historic_data = model.data.to_dict(orient='records')
        filtered_historic_data = list(filter(lambda x: x['date'] > six_months_ago, historic_data))

        r = {
            'version': __version__,
            'success': True,
            'message': 'Historic Bitcoin prices from CoinMarketCap.',
            'start_date': os.getenv('BITCOIN_START_DATE'),
            'result': filtered_historic_data
        }

        return jsonify(r)

    @cache.cached(timeout=60 * 24, key_prefix=__cache_identifier)
    @app.route('/predict')
    def predict():
        """
        Endpoint for predicting bitcoin prices.
        """
        r = {
            'version': __version__,
            'success': True,
            'message': 'Endpoint for making predictions.',
            'period_length': os.getenv('PERIOD_SIZE', 7),
            'result': model.predict(denormalized=True, return_dict=True)
        }
        return jsonify(r)
