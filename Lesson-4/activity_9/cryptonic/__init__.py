"""
Cryptonic is an educational application created for 
the purposes of learning how to use deep learning
to predict Bitcoin prices.
"""
from cryptonic.models.model import Model
from cryptonic.markets.coinmarketcap import CoinMarketCap

__version__ = 'v1.0.1'
__author__ = 'Luis Capelo'
__email__ = 'luiscape@gmail.com'

__all__ = ['Model', 'CoinMarketCap']
