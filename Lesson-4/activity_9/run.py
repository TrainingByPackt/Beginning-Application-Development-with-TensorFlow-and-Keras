#!/usr/bin/python
"""
Script for starting the Cryptonic Flask server.
"""
import os
import time

from cryptonic.server import Server


def main():
    """
    Wrapper function for starting a server.
    """

    print('Starting server.')
    server = Server()
    
    server.run(host=os.getenv('HOST', '0.0.0.0'))

if __name__ == '__main__':
    main()
