.. alpha_vantage documentation master file, created by
   sphinx-quickstart on Sun May 28 14:23:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to alpha_vantage's documentation!
=========================================

|Build Status| |PyPI version| |Documentation Status|

*Python module to get stock data from the Alpha Vantage API*
Alpha Vantage http://www.alphavantage.co/ is a free JSON APIs for stock market
data, plus a comprehensive set of technical indicators. This project is a python wrapper
around this API to offer python plus json/pandas support. I hope you enjoy it.
It requires a free API, that can be
requested on http://www.alphavantage.co/support/#api-key.

Install
-------

To install the package use:

.. code:: shell

    pip install alpha_vantage

If you want to install from source, then use:

.. code:: shell

    git clone https://github.com/RomelTorres/alpha_vantage.git
    pip install -e alpha_vantage


Usage Example
=============
This is a simple code snippet to get global quotes from the

.. code:: python

    from alpha_vantage.timeseries import TimeSeries
    import matplotlib.pyplot as plt

    ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
    data['close'].plot()
    plt.title('Intraday Times Series for the MSFT stock (1 min)')
    plt.show()


Code & Issue Tracker
====================
The code is hosted in github: https://github.com/RomelTorres/alpha_vantage
And the issue tracker as well: https://github.com/RomelTorres/alpha_vantage/issues

Contributions
=============
If you have a feature that you want to see merged in the code, please do a pull
request with it and it will be evaluated.

License
=======
This project is licensed under the MIT license.

Contents
========
.. toctree::
    :maxdepth: 4


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Documentation
-------------

To find out more about the available api calls, visit the alpha-vantage
documentation at http://www.alphavantage.co/documentation/



.. |Build Status| image:: https://travis-ci.org/RomelTorres/alpha_vantage.png?branch=master
   :target: https://travis-ci.org/RomelTorres/alpha_vantage
.. |PyPI version| image:: https://badge.fury.io/py/alpha_vantage.svg
   :target: https://badge.fury.io/py/alpha_vantage
.. |Documentation Status| image:: https://readthedocs.org/projects/alpha-vantage/badge/?version=latest
   :target: http://alpha-vantage.readthedocs.io/en/latest/?badge=latest
