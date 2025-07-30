"""
APISIX Python Client
~~~~~~~~~~~~~~~~~~~

A simple Python client for Apache APISIX.

Usage:
    >>> from apisix_client import ApisixClient
    >>> client = ApisixClient('http://localhost:9080/apisix/admin', 'edd1c9f034335f136f87ad84b625c8f1')
    >>> routes = client.list_routes()
"""

from .client import ApisixClient

__version__ = '0.1.0'
__all__ = ['ApisixClient']