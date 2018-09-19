"""
Logic for collecting data directly from the 
CoinMarketCap API.
"""
import requests
import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup


class CoinMarketCap:
    """
    Class interface to data from CoinMarketCap. 
    Original data can be found at:

        https://coinmarketcap.com/
    
    """
    def __repr__(self):
        message = """

        Crypto-currency data comes from the website CoinMarketCap.
        CoinMarketCap is can be accessed at: https://coinmarketcap.com/

        The permission to use the data is available on their FAQ

            https://coinmarketcap.com/faq/

        and reads:

            "Q: Am I allowed to use content (screenshots, data, graphs, etc.) 
            for one of my personal projects and/or commercial use?

            R: Absolutely! Feel free to use any content as you see fit. 
            We kindly ask that you cite us as a source."
        
        """
        return message

    @classmethod
    def historic(cls, start='2013-04-28', stop=None, ticker='bitcoin', return_json=False):
        """
        Retrieves historic data within a time
        period.

        Parameters
        ----------
        start, stop: str
            Start and stop dates in ISO format (YYYY-MM-DD).

        ticker: str
            Name of ticker to be used (e.g. `bitcoin`).
        
        Returns
        -------
        Pandas dataframe with historical ticker data.
        """
        start = start.replace('-', '')
        if not stop:
            stop = datetime.now().strftime('%Y%m%d')

        url = 'https://coinmarketcap.com/currencies/{}/historical-data/?start={}&end={}'.format(ticker, start, stop)
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find_all('table')[0]
        df = pd.read_html(str(table))[0]
        
        #
        #  Cleans variables from the original.
        #
        df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%b %d, %Y').strftime('%Y-%m-%d'))
        df['Volume'] = df['Volume'].apply(lambda x: None if x == '-' else x)
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'market_cap']

        if return_json:
            df.to_json(orient='records')

        return df

    @classmethod
    def current(cls, ticker='bitcoin'):
        """
        Fetches current prices from CoinMarketCap.

        Returns
        -------
        Dictionary with a single record form the 
        """
        url = 'https://api.coinmarketcap.com/v1/ticker/{}/'.format(ticker)
        r = requests.get(url)

        return r.json()
